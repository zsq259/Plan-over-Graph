test_case="50-1-100"
output_dir="data/result/llama-31-8b-instruct-sft14"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "/home/zhangsq/1/LLaMA-Factory/saves/llama3-8b/merged_models/llama3_lora_sft_abstask"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\