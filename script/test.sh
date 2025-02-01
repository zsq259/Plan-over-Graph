test_case="50-1-100-t"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "/data/share/data/llama-factory/LLaMA-Factory/saves/llama3-8b/lora/merged_model/abstask_dpo_12000_6000"\
    --scheduler parallel\
    --max_retry 3\
    --test_case "${test_case}"\
    --test_file "data/dev/${test_case}.json"\
    --output_dir "data/result/llama-31-8b-instruct-sft24"\