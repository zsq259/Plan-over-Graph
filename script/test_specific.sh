test_case="10-1-100-s"
output_dir="data/result/deepseek-reasoner"

python -m src.main\
    --task specific_task\
    --template specific_task_plan\
    --model "deepseek-reasoner"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\