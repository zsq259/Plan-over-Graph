test_case="10-1-100-s"

python -m src.agent.main\
    --task specific_task\
    --template abstask_plan\
    --model "meta-llama/Llama-3.1-8B-Instruct"\
    --scheduler parallel\
    --max_retry 2\
    --extractor 1\
    --test_case "${test_case}"\
    --test_file "data/dev/${test_case}.json"\
    --output_dir "data/result/llama-31-8b-instruct"\