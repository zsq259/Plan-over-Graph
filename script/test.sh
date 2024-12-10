test_case="50-1-100"
output_dir="data/abstask/result/llama-31-8b-instruct-prompt3"

python -m src.main\
    --task abstask\
    --template "abstask_plan_ref"\
    --model "meta-llama/Meta-Llama-3.1-8B-Instruct"\
    --scheduler parallel\
    --test_file "data/abstask/dev/${test_case}.json"\
    --output_file "${output_dir}/${test_case}-output.json"\