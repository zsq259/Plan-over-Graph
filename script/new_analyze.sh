export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
python -m src.new_analyze --model_name "deepseek-reasoner" 
unset LD_LIBRARY_PATH