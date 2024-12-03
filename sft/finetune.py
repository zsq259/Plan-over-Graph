"""
llama3微调
"""
import os
import argparse
import torch
import torch.nn.functional as F
import datasets
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from torch.utils.tensorboard import SummaryWriter
from transformers.integrations import TensorBoardCallback
from transformers import PreTrainedTokenizerBase
from dataclasses import dataclass, field
from transformers import AutoTokenizer, AutoModel
from peft import get_peft_model, LoraConfig, TaskType
from transformers import Trainer, HfArgumentParser
from unsloth import FastLanguageModel

@dataclass
class DataCollator:
    tokenizer: PreTrainedTokenizerBase
    max_seq_length: int = 12800

    def __call__(self, features: list) -> dict:
        len_ids = [len(feature["input_ids"]) for feature in features]
        longest = max(len_ids)
        input_ids = []
        labels_list = []
        for ids_l, feature in sorted(zip(len_ids, features), key=lambda x: -x[0]):
            ids = feature["input_ids"]
            seq_len = feature["seq_len"]
            if seq_len >= self.max_seq_length:
                print(f"Input sequence length {seq_len} exceeds the maximum sequence length {self.max_seq_length}.")
                ids = ids[:self.max_seq_length]
                seq_len = self.max_seq_length
            # 仅计算label部分的损失
            labels = (
                    [-100] * (seq_len - 1)
                    + ids[(seq_len - 1):]
                    + [-100] * (longest - ids_l)
            )
            ids = ids + [self.tokenizer.pad_token_id] * (longest - ids_l)
            _ids = torch.LongTensor(ids)
            labels_list.append(torch.LongTensor(labels))
            input_ids.append(_ids)
        input_ids = torch.stack(input_ids)
        labels = torch.stack(labels_list)
        return {
            "input_ids": input_ids,
            "labels": labels,
        }


class ModifiedTrainer(Trainer):
    """
    自定义trainer，优化后的损失函数
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        # 获取模型的输出
        outputs = model(
            input_ids=inputs["input_ids"],
            labels=inputs["labels"],
        )
        logits = outputs.logits
        labels = inputs["labels"]
        
        # 计算交叉熵损失
        loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
        loss = loss_fct(logits.view(-1, logits.size(-1)), labels.view(-1))
        
        # 计算每个位置的熵
        softmax_probs = F.softmax(logits, dim=-1)
        entropy = -torch.sum(softmax_probs * torch.log(softmax_probs + 1e-8), dim=-1)
        entropy = entropy.view(-1)
        
        # 创建权重张量，初始值为1
        weights = torch.ones_like(loss)
        
        tokenizer = self.processing_class
        n_token_id = tokenizer.convert_tokens_to_ids('N')
        number_token_ids = [tokenizer.convert_tokens_to_ids(str(i)) for i in range(10)]
        
        # 找到标签中所有'N'的位置
        labels_flat = labels.view(-1)
        n_positions = (labels_flat == n_token_id).nonzero(as_tuple=False).squeeze()
        
        # 定义较大的权重，用于数字部分
        large_weight = 10.0
        
        # 增加'N'后面的数字位置的权重
        for pos in n_positions:
            if pos + 1 < labels_flat.size(0):  # 确保下一个位置存在
                next_label = labels_flat[pos + 1]
                if next_label in number_token_ids:  # 如果下一个标签是数字
                    weights[pos + 1] = large_weight
        
        # 动态调整权重：根据熵来加权
        adjust_positions = (weights == large_weight)
        weights[adjust_positions] *= torch.exp(entropy[adjust_positions])
        
        # 计算加权损失
        weighted_loss = (loss * weights).mean()
        
        return weighted_loss


    def save_model(self, output_dir=None, _internal_call=False):
        from transformers.trainer import TRAINING_ARGS_NAME

        os.makedirs(output_dir, exist_ok=True)
        torch.save(self.args, os.path.join(output_dir, TRAINING_ARGS_NAME))
        saved_params = {
            k: v.to("cpu") for k, v in self.model.named_parameters() if v.requires_grad
        }
        torch.save(saved_params, os.path.join(output_dir, "adapter_model.bin"))


class Llama3Fintune(object):
    """
    Llama3微调
    """

    def __init__(self):
        pass

    def train(self):
        """
        训练入口
        :return:
        """
        
        writer = SummaryWriter()
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name="/home/zhangsq/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3.1-8B-Instruct/snapshots/0e9e39f249a16976918f6564b8830bc894c89659", max_seq_length=12800,
            dtype=None, load_in_4bit=True)
        dataset = datasets.load_from_disk("/home/zhangsq/1/test/play/llama3_train_tokenize")
        eval_dataset = datasets.load_from_disk("/home/zhangsq/1/test/play/llama3_eval_tokenize")  # 加载验证集数据
        # 配置lora参数
        model = FastLanguageModel.get_peft_model(
            model,
            # 低秩表征：Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
            r=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj", ],
            lora_alpha=16,
            lora_dropout=0,  # Supports any, but = 0 is optimized
            # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
            use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
            random_state=3407,
            use_rslora=False,  # We support rank stabilized LoRA
            loftq_config=None,  # And LoftQ
            inference_mode=False,
        )
        # 模型训练参数配置
        # trl框架的SFTTrainer
        # trainer = SFTTrainer(
        #     model=model,
        #     tokenizer=tokenizer,
        #     train_dataset=dataset,
        #     dataset_text_field="text",
        #     max_seq_length=5000,
        #     dataset_num_proc=2,
        #     packing=False,  # Can make training 5x faster for short sequences.
        #     args=TrainingArguments(
        #         per_device_train_batch_size=2,
        #         gradient_accumulation_steps=4,
        #         warmup_steps=5,
        #         max_steps=1,
        #         learning_rate=2e-4,
        #         fp16=not torch.cuda.is_bf16_supported(),
        #         bf16=torch.cuda.is_bf16_supported(),
        #         logging_steps=1,
        #         optim="adamw_8bit",
        #         weight_decay=0.01,
        #         lr_scheduler_type="linear",
        #         seed=3407,
        #         output_dir="lora_trained_llama31",
        #         # num_train_epochs=3
        #     ),
        # )
        # 自定义损失的Trainer
        train_args = TrainingArguments(
            remove_unused_columns=False,
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            # max_steps=52000,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=100,
            optim="adamw_torch",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir="lora_trained_llama31_8B",
            num_train_epochs=10,
            save_steps=500,
            eval_steps=500,
            evaluation_strategy="steps",
        )
        trainer = ModifiedTrainer(
            model=model,
            train_dataset=dataset,
            eval_dataset=eval_dataset,  # 添加验证集
            args=train_args,
            callbacks=[TensorBoardCallback(writer)],
            data_collator=DataCollator(tokenizer),
            processing_class=tokenizer,
        )
        # 开始训练
        trainer.train()
        writer.close()
        # 存储微调模型至文件夹
        model.save_pretrained("lora_trained_llama31_8B")

if __name__ == '__main__':
    Llama3Fintune().train()
