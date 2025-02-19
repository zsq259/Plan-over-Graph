test_case="50-1-100-t"

python -m src.agent.main\
    --task abstask\
    --template abstask_plan\
    --model "meta-llama/Llama-3.1-8B-Instruct"\
    --scheduler parallel\
    --max_retry 3\
    --test_case "${test_case}"\
    --test_file "data/dev/test/${test_case}.json"\
    --output_dir "data/result/llama-31-8b-instruct"\