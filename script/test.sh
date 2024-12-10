python -m src.main\
    --task abstask\
    --template "abstask_plan"\
    --model "meta-llama/Meta-Llama-3.1-8B-Instruct"\
    --scheduler parallel\
    --test_file "/home/zhangsq/1/test/data/abstask/dev/30-1-100.json"\
    --output_file "/home/zhangsq/1/test/data/abstask/result/llama-31-8b-instruct-prompt/30-1-100c-output.json"\