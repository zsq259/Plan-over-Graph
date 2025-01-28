test_case="50-1-100"
output_dir="data/result/deepseek-reasoner"

python -m src.main\
    --task abstask\
    --template abstask_plan\
    --model "deepseek-reasoner"\
    --scheduler parallel\
    --test_file "data/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\