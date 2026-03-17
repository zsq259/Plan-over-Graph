# Plan-over-Graph: Towards Parallelable LLM Agent Schedule

Code and data for the paper "Plan-over-Graph: Towards Parallelable LLM Agent Schedule". [[paper]](https://arxiv.org/abs/2502.14563)

Large Language Models (LLMs) have demonstrated exceptional abilities in reasoning for task planning. However, challenges remain under-explored for parallel schedules. This paper introduces a novel paradigm, $\textit{plan-over-graph}$, in which the model first decomposes a real-life textual task into executable subtasks and constructs an abstract task graph. The model then understands this task graph as input and generates a plan for parallel execution. To enhance the planning capability of complex, scalable graphs, we design an automated and controllable pipeline to generate synthetic graphs and propose a two-stage training scheme. Experimental results show that our $\textit{plan-over-graph}$ method significantly improves task performance on both API-based LLMs and trainable open-sourced LLMs. By normalizing complex tasks as graphs, our method naturally supports parallel execution, demonstrating global efficiency.

### Running the Code

1. Clone the repository:
```bash
git clone https://github.com/zsq259/Plan-over-Graph.git
cd Plan-over-Graph
```
2. Create a virtual environment and install dependencies:
```bash
conda create -n planovergraph python=3.12
conda activate planovergraph
pip install -r requirements.txt
```
3. Download the dataset:
```bash
mkdir data && cd data
wget https://huggingface.co/datasets/hastin/plan-over-graph/resolve/main/data.zip 
unzip data.zip && rm data.zip
cd ..
```
> We provide our results in `data/result/` folder for your reference.
4. Run the testing script:
You can run the testing script to evaluate the model on the test set.
```bash
./script/test.sh # script for testing abstract graph
./script/test_query.sh # script for testing textual query without extraction
./script/test_query_extract.sh # script for testing textual query with extraction
```

### Citation
If you find this code useful for your research, please consider citing our paper:
```bibtex
@misc{zhang2025planovergraphparallelablellmagent,
      title={Plan-over-Graph: Towards Parallelable LLM Agent Schedule}, 
      author={Shiqi Zhang and Xinbei Ma and Zouying Cao and Zhuosheng Zhang and Hai Zhao},
      year={2025},
      eprint={2502.14563},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2502.14563}, 
}
```
