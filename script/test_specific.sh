test_case="30-1-100-s"

python -m src.agent.main\
    --task specific_task\
    --template specific_task_plan\
    --model "meta-llama/Llama-3.1-8B-Instruct"\
    --max_retry 2\
    --scheduler parallel\
    --test_case "${test_case}"\
    --test_file "data/dev/test/${test_case}.json"\
    --output_dir "data/result/Llama-3.1-8B-Instruct"
