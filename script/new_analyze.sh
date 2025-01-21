export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
python -m src.new_analyze --model_name "llama-31-8b-instruct-sft11" --file_prefixes 10-1-100 30-1-100 50-1-100
unset LD_LIBRARY_PATH