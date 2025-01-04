test_case="50-1-100"
output_dir="data/result/llama-31-8b-instruct-prompt3"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "/home/maxb/hst/LLaMA-Factory/saves/llama3-8b/lora/dpo"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\