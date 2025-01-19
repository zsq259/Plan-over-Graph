test_case="30-1-100-t"
output_dir="data/result/llama-31-8b-instruct-sft15"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "/data/share/data/llama-factory/LLaMA-Factory/saves/llama3-8b/lora/merged_model/sft_3000"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\