test_case="30-3-1000"
output_dir="data/abstask/result/llama-31-8b-instruct-sft11"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "/data/share/maxb/LLaMA-Factory/merged-model/llama3_lora_sft2"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\