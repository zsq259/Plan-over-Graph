import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForCausalLM

# 加载预训练模型和分词器
model_name = 'gpt2'  # 可根据需要更改模型名称
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def compute_loss(model_output_text, reference_text):
    # 将文本编码为输入 ID
    input_ids = tokenizer.encode(model_output_text, return_tensors='pt')
    labels = tokenizer.encode(reference_text, return_tensors='pt')
    
    # 确保 input_ids 和 labels 长度一致
    min_length = min(input_ids.size(1), labels.size(1))
    input_ids = input_ids[:, :min_length]
    labels = labels[:, :min_length]
    
    # 获取模型输出的 logits
    with torch.no_grad():
        outputs = model(input_ids)
    logits = outputs.logits
    
    # 调整 logits 和 labels 的形状
    logits = logits.view(-1, logits.size(-1))
    labels = labels.view(-1)
    
    # 计算交叉熵损失
    loss_fn = nn.CrossEntropyLoss()
    loss = loss_fn(logits, labels)
    
    return loss.item()

# 示例调用
model_output_text = "这是模型生成的文本。"
reference_text = "这是标准答案的文本。"
loss_value = compute_loss(model_output_text, reference_text)
print(f"损失值: {loss_value}")