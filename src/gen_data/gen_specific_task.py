import json
from template.specific_task import instruction, example_task

def gen_specific_task(task, model):
    prompt = instruction.format(example=example_task, task=task)
    print(prompt)
    response = model.predict(prompt)
    return response

def main():
    # task = {'rules': [{'source': ['N1'], 'target': ['N2'], 'time': 13, 'cost': 1}, {'source': ['N2', 'N1'], 'target': ['N3'], 'time': 44, 'cost': 1}, {'source': ['N1', 'N3'], 'target': ['N4'], 'time': 40, 'cost': 1}, {'source': ['N2', 'N3'], 'target': ['N5'], 'time': 3, 'cost': 1}, {'source': ['N3', 'N1'], 'target': ['N6'], 'time': 11, 'cost': 1}, {'source': ['N5', 'N4'], 'target': ['N6'], 'time': 4, 'cost': 1}, {'source': ['N5'], 'target': ['N7'], 'time': 22, 'cost': 1}, {'source': ['N2'], 'target': ['N7'], 'time': 40, 'cost': 1}, {'source': ['N6', 'N1'], 'target': ['N8'], 'time': 50, 'cost': 1}, {'source': ['N7', 'N3'], 'target': ['N9'], 'time': 28, 'cost': 1}, {'source': ['N4', 'N8'], 'target': ['N9'], 'time': 28, 'cost': 1}, {'source': ['N1', 'N5'], 'target': ['N9'], 'time': 21, 'cost': 1}, {'source': ['N4'], 'target': ['N10'], 'time': 48, 'cost': 1}, {'source': ['N9'], 'target': ['N10'], 'time': 5, 'cost': 1}], 'initial_source': ['N1'], 'target': 'N10'}
    file_path = "data/dev/test/30-1-100-r.json"
    output_file = "data/dev/30-1-100-s_2.json"
    from src.agent.model.gpt_wrapper import GPTWrapper
    # model = GPTWrapper("deepseek-reasoner")
    model = GPTWrapper("claude-3-5-sonnet-20241022")
    data = json.load(open(file_path))
    results = []
    # for d in data:
    #     if "story" in d:
    #         results.append(d)
    #         continue
    #     print("id: ", d["id"])
    #     task = d["question"]
    #     response = gen_specific_task(task, model)
    #     print(response)
    #     new_d = d.copy()
    #     new_d["story"] = response
    #     results.append(new_d)
    #     with open(output_file, "w") as f:
    #         json.dump(results, f, indent=4)
        
    import random
    d = random.choice(data)
    while len(d["question"]["rules"]) < 20 or len(d["question"]["rules"]) > 22:
        d = random.choice(data)
    task = d["question"]
    print(len(d["question"]["rules"]))
    response = gen_specific_task(task, model)
    print(response)
    with open("1.txt", "w") as f:
        f.write(response)
    
if __name__ == "__main__":
    main()
    