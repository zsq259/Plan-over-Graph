python -m src.main\
    --task abstask\
    --model "/home/zhangsq/1/test/lora_trained_llama31_1/checkpoint-1250"\
    --scheduler parallel\
    --test_file "/home/zhangsq/1/test/data/abstask/dev/30-3-100.json"\
    --output_file "/home/zhangsq/1/test/data/abstask/result/llama-31-8b-instruct-sft2/30-3-100-output.json"\