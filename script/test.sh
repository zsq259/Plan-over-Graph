python -m src.main\
    --task hotpotqa\
    --model "gpt-3.5-turbo-instruct"\
    --scheduler parallel\
    --test_file "data/hotpotqa/small_test.json"\
    --output_file "data/hotpotqa/output.json"\