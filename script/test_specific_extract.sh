test_case="10-1-100-s"

python -m src.main\
    --task specific_task\
    --template abstask_plan\
    --model "/data/share/data/llama-factory/LLaMA-Factory/saves/llama3-8b/lora/merged_model/abstask_dpo_12000_6000"\
    --scheduler parallel\
    --extractor "/data/share/data/llama-factory/LLaMA-Factory/Meta-Llama-3.1-8B-Instruct"\
    --test_case "${test_case}"\
    --test_file "data/dev/${test_case}.json"\
    --output_dir "data/result/llama-31-8b-instruct-sft24"\