import argparse
import json
from tqdm import tqdm

import datasets
import transformers
import os


def preprocess(tokenizer, config, example, max_seq_length, version):
    if version == 'v1':
        prompt = example["context"]
        target = example["target"]
        prompt_ids = tokenizer.encode(prompt, max_length=max_seq_length, truncation=True)
        target_ids = tokenizer.encode(
            target,
            max_length=max_seq_length,
            truncation=True,
            add_special_tokens=False)
        input_ids = prompt_ids + target_ids
        input_ids.extend([tokenizer.eos_token_id])
        return {"input_ids": input_ids, "seq_len": len(prompt_ids)}

    if version == 'v2':
        query = example["context"]
        target = example["target"]
        history = None
        prompt = tokenizer.build_prompt(query, history)

        a_ids = tokenizer.encode(text=prompt, add_special_tokens=True, truncation=True,
                                 max_length=max_seq_length)
        b_ids = tokenizer.encode(text=target, add_special_tokens=False, truncation=True,
                                 max_length=max_seq_length)

        input_ids = a_ids + b_ids + [tokenizer.eos_token_id]

        return {"input_ids": input_ids, "seq_len": len(a_ids)}


def read_jsonl(path, max_seq_length, base_model_path, version='v1', skip_overlength=False):

    tokenizer = transformers.AutoTokenizer.from_pretrained(
        base_model_path, trust_remote_code=True)
    config = transformers.AutoConfig.from_pretrained(
        base_model_path, trust_remote_code=True, device_map='auto')
    fuck = None
    with open(path, "r") as f:
        for line in tqdm(f.readlines()):
            example = json.loads(line)
            print(example)
            # feature = preprocess(tokenizer, config, example, max_seq_length)
            feature = preprocess(tokenizer, config, example, max_seq_length, version)
            # print(type(feature["input_ids"]), type(feature["seq_len"]))
            # print(fuck)
            if not fuck:
                print(feature["input_ids"])
                fuck = 1
            if skip_overlength and len(feature["input_ids"]) > max_seq_length:
                continue
            # feature["input_ids"] = feature["input_ids"][:max_seq_length]
            yield feature


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl_path", type=str, default="/home/zhangsq/1/test/play/samples_eval_llama.jsonl")
    parser.add_argument("--save_path", type=str, default="/home/zhangsq/1/test/play/llama3_eval_tokenize")
    parser.add_argument("--max_seq_length", type=int, default=12800)
    parser.add_argument("--skip_overlength", type=bool, default=True)
    parser.add_argument("--base_model", type=str, default="/home/zhangsq/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3.1-8B-Instruct/snapshots/0e9e39f249a16976918f6564b8830bc894c89659")
    parser.add_argument("--version", type=str, default='v1')
    args = parser.parse_args()

    dataset = datasets.Dataset.from_generator(
        lambda: read_jsonl(args.jsonl_path, args.max_seq_length, args.base_model, args.version, args.skip_overlength)
    )
    dataset.save_to_disk(args.save_path)


if __name__ == "__main__":
    main()
