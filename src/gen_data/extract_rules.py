import json, os
from src.agent.model.gpt_wrapper import GPTWrapper
from src.agent.model.llama_wrapper import LlamaWrapper
from src.agent.module.extractor import Extractor
from src.utils.utils import compare_rule_sets, extract_json

def file_extract(extractor, file_path, output_path):
    data = json.load(open(file_path, "r"))

    results = []
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            results = json.load(f)
    
    exist_ids = set([r['id'] for r in results])
    
    for d in data:
        if d['id'] in exist_ids:
            continue
        task = d['story']
        try:
            rules = extractor.extract(task)
            d['model_rules'] = rules
            valid = compare_rule_sets(rules, d['question'])
            d['valid'] = valid
            results.append(d)
            with open(output_path, "w") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error extracting rules for id {d['id']}: {e}")
            continue

def text_extract(extractor, text):
    rules = extractor.extract(text)
    return rules


def main():
    model = GPTWrapper("deepseek-reasoner")
    # model = LlamaWrapper()
    extractor = Extractor(model)

    # file_path = "data/dev/10-1-100-s.json"
    # output_path = "data/result/llama-31-8b-instruct/10-1-100-s.json"
    # file_extract(extractor, file_path, output_path)


    rules = """
    ```json
    {'rules': [{'id': 0, 'source': ['N1'], 'target': ['N2'], 'time': 17, 'cost': 1}, {'id': 1, 'source': ['N1'], 'target': ['N3'], 'time': 44, 'cost': 1}, {'id': 2, 'source': ['N3'], 'target': ['N4'], 'time': 31, 'cost': 1}, {'id': 3, 'source': ['N4'], 'target': ['N5'], 'time': 10, 'cost': 1}, {'id': 4, 'source': ['N3', 'N4'], 'target': ['N6'], 'time': 30, 'cost': 1}, {'id': 5, 'source': ['N1'], 'target': ['N7'], 'time': 42, 'cost': 1}, {'id': 6, 'source': ['N7', 'N1'], 'target': ['N8'], 'time': 46, 'cost': 1}, {'id': 7, 'source': ['N6'], 'target': ['N9'], 'time': 50, 'cost': 1}, {'id': 8, 'source': ['N3'], 'target': ['N10'], 'time': 48, 'cost': 1}, {'id': 9, 'source': ['N7', 'N1'], 'target': ['N11'], 'time': 45, 'cost': 1}, {'id': 10, 'source': ['N11', 'N5', 'N9'], 'target': ['N12'], 'time': 9, 'cost': 1}, {'id': 11, 'source': ['N1'], 'target': ['N13'], 'time': 33, 'cost': 1}, {'id': 12, 'source': ['N10', 'N1'], 'target': ['N14'], 'time': 49, 'cost': 1}, {'id': 13, 'source': ['N3', 'N7'], 'target': ['N14'], 'time': 50, 'cost': 1}, {'id': 14, 'source': ['N10', 'N6'], 'target': ['N15'], 'time': 19, 'cost': 1}, {'id': 15, 'source': ['N10', 'N3'], 'target': ['N16'], 'time': 44, 'cost': 1}, {'id': 16, 'source': ['N8', 'N6'], 'target': ['N17'], 'time': 16, 'cost': 1}, {'id': 17, 'source': ['N4', 'N7', 'N15'], 'target': ['N17'], 'time': 3, 'cost': 1}, {'id': 18, 'source': ['N5', 'N7', 'N13'], 'target': ['N18'], 'time': 47, 'cost': 1}, {'id': 19, 'source': ['N3', 'N14'], 'target': ['N19'], 'time': 34, 'cost': 1}, {'id': 20, 'source': ['N9', 'N8', 'N13', 'N7'], 'target': ['N20'], 'time': 45, 'cost': 1}, {'id': 21, 'source': ['N1', 'N12'], 'target': ['N21'], 'time': 28, 'cost': 1}, {'id': 22, 'source': ['N10', 'N19'], 'target': ['N21'], 'time': 7, 'cost': 1}, {'id': 23, 'source': ['N18', 'N4'], 'target': ['N22'], 'time': 33, 'cost': 1}, {'id': 24, 'source': ['N6', 'N3'], 'target': ['N22'], 'time': 29, 'cost': 1}, {'id': 25, 'source': ['N8', 'N12'], 'target': ['N22'], 'time': 50, 'cost': 1}, {'id': 26, 'source': ['N15', 'N22', 'N7'], 'target': ['N23'], 'time': 35, 'cost': 1}, {'id': 27, 'source': ['N5', 'N17', 'N1', 'N19'], 'target': ['N23'], 'time': 28, 'cost': 1}, {'id': 28, 'source': ['N13', 'N22'], 'target': ['N24'], 'time': 45, 'cost': 1}, {'id': 29, 'source': ['N5', 'N7'], 'target': ['N24'], 'time': 10, 'cost': 1}, {'id': 30, 'source': ['N3', 'N14'], 'target': ['N24'], 'time': 30, 'cost': 1}, {'id': 31, 'source': ['N3', 'N19'], 'target': ['N25'], 'time': 41, 'cost': 1}, {'id': 32, 'source': ['N2', 'N6', 'N17'], 'target': ['N25'], 'time': 10, 'cost': 1}, {'id': 33, 'source': ['N5', 'N20'], 'target': ['N25'], 'time': 38, 'cost': 1}, {'id': 34, 'source': ['N19', 'N9', 'N20', 'N8'], 'target': ['N26'], 'time': 23, 'cost': 1}, {'id': 35, 'source': ['N15', 'N22'], 'target': ['N27'], 'time': 24, 'cost': 1}, {'id': 36, 'source': ['N24', 'N25'], 'target': ['N27'], 'time': 46, 'cost': 1}, {'id': 37, 'source': ['N16', 'N15', 'N1', 'N4'], 'target': ['N28'], 'time': 30, 'cost': 1}, {'id': 38, 'source': ['N4', 'N7'], 'target': ['N29'], 'time': 37, 'cost': 1}, {'id': 39, 'source': ['N27', 'N8', 'N14'], 'target': ['N29'], 'time': 22, 'cost': 1}, {'id': 40, 'source': ['N17', 'N2'], 'target': ['N30'], 'time': 14, 'cost': 1}], 'initial_source': ['N1'], 'target': 'N23'}
    ```
    """

    text = """
    At a major game studio, the "Core Gameplay System(N23)" development begins with the "Game Engine(N1)" as the foundation. The engine team can pursue several parallel paths: they can develop the "Physics System(N2)" in 17 days at a cost of 1, create the "Graphics Engine(N3)" in 44 days at a cost of 1, set up the "Sound System(N7)" in 42 days at a cost of 1, or establish the "Network Framework(N13)" in 33 days at a cost of 1.

    Once the "Graphics Engine(N3)" is ready, it enables development of the "Animation System(N4)" in 31 days at a cost of 1. This "Animation System(N4)" then allows creation of the "Character Movement(N5)" in 10 days at a cost of 1. The "Graphics Engine(N3)" and "Animation System(N4)" together enable development of the "Rendering Pipeline(N6)" in 30 days at a cost of 1.

    The "Sound System(N7)" and "Game Engine(N1)" jointly enable creation of the "Audio Manager(N8)" in 46 days at a cost of 1 and the "Resource Manager(N11)" in 45 days at a cost of 1. The "Rendering Pipeline(N6)" leads to the "Shader System(N9)" development in 50 days at a cost of 1.

    The "Graphics Engine(N3)" also enables creation of the "Particle System(N10)" in 48 days at a cost of 1. This "Particle System(N10)" and "Game Engine(N1)" together allow development of the "Effects Engine(N14)" in 49 days at a cost of 1, while the "Graphics Engine(N3)" and "Sound System(N7)" can also create this "Effects Engine(N14)" through a different route in 50 days at a cost of 1.

    The "Particle System(N10)" and "Rendering Pipeline(N6)" enable creation of the "Visual Effects System(N15)" in 19 days at a cost of 1. The "Particle System(N10)" and "Graphics Engine(N3)" together create the "Environmental System(N16)" in 44 days at a cost of 1.

    The "Audio Manager(N8)" and "Rendering Pipeline(N6)" enable development of the "Game State Manager(N17)" in 16 days at a cost of 1. Alternatively, the "Animation System(N4)," "Sound System(N7)," and "Visual Effects System(N15)" can create this "Game State Manager(N17)" in just 3 days at a cost of 1.

    The "Resource Manager(N11)," "Character Movement(N5)," and "Shader System(N9)" together enable creation of the "Asset Management System(N12)" in 9 days at a cost of 1. When the "Character Movement(N5)," "Sound System(N7)," and "Network Framework(N13)" are ready, they enable creation of the "Input System(N18)" in 47 days at a cost of 1.

    The "Graphics Engine(N3)" and "Effects Engine(N14)" allow development of the "Camera System(N19)" in 34 days at a cost of 1. The "Shader System(N9)," "Audio Manager(N8)," "Network Framework(N13)," and "Sound System(N7)" together create the "Level Loading System(N20)" in 45 days at a cost of 1.

    The "Game Engine(N1)" and "Asset Management System(N12)" enable creation of the "Memory Management(N21)" in 28 days at a cost of 1. Alternatively, the "Particle System(N10)" and "Camera System(N19)" can create this "Memory Management(N21)" in 7 days at a cost of 1.

    Multiple paths lead to the "AI System(N22)": the "Input System(N18)" and "Animation System(N4)" can create it in 33 days at a cost of 1, the "Rendering Pipeline(N6)" and "Graphics Engine(N3)" can do it in 29 days at a cost of 1, or the "Audio Manager(N8)" and "Asset Management System(N12)" can achieve it in 50 days at a cost of 1.

    Finally, the "Core Gameplay System(N23)" can be completed through two different routes: either the "Visual Effects System(N15)," "AI System(N22)," and "Sound System(N7)" can create it in 35 days at a cost of 1, or the "Character Movement(N5)," "Game State Manager(N17)," "Game Engine(N1)," and "Camera System(N19)" can complete it in 28 days at a cost of 1.

    Additional systems like the "Debug Tools(N24)," "Performance Profiler(N25)," "Collision System(N26)," "Physics Solver(N27)," "Scene Graph(N28)," "Entity Component System(N29)," and "Event System(N30)" are developed in parallel but aren't required for the core gameplay completion.

    """
    rules = extract_json(rules)
    print(rules)
    extracted_rules = text_extract(extractor, text)
    print(extracted_rules)
    valid = compare_rule_sets(extracted_rules, rules)
    print(valid)
    
            
if __name__ == "__main__":
    main()