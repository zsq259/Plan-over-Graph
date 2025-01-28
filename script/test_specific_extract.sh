test_case="10-1-100-s_2"
output_dir="data/result/deepseek-chat"

python -m src.main\
    --task specific_task\
    --template abstask_plan\
    --model "deepseek-chat"\
    --scheduler parallel\
    --extractor true\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\