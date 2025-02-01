test_case="10-1-100-s-filtered"

python -m src.main\
    --task specific_task\
    --template specific_task_plan\
    --model "/data/share/data/llama-factory/LLaMA-Factory/Meta-Llama-3.1-8B-Instruct"\
    --scheduler parallel\
    --test_case "${test_case}"\
    --test_file "data/dev/${test_case}.json"\
    --output_dir "data/result/llama-31-8b-instruct-sft18"\