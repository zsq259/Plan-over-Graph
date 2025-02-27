instruction = """
You are given a set of transformation rules, where each rule consists of source nodes (materials or subtasks), target nodes (resulting materials or tasks), the time required to complete the transformation, and a cost associated with the transformation. Your goal is to plan a path from the initial nodes to the target node, supporting parallel transformations, to obtain the target node in the shortest time possible, while minimizing the total cost.
Input format:
- Transformation rules: A list of dictionaries, where each dictionary represents a transformation rule and contains:
  - source: A list of source nodes (the prerequisites for the transformation).
  - target: A list of target nodes (the result of the transformation).
  - time: The time required to complete the transformation (an integer).
  - cost: The cost associated with the transformation (an integer).

- Initial nodes: A list of strings representing the available nodes at the start.

- Target node: A string representing the node that needs to be obtained.

Output format:
- Plan: A list of subtasks, where each subtask is a JSON object with the following fields:
  - name: The name of the subtask or node being completed.
  - source: A list of source nodes involved in this subtask.
  - target: The target node resulting from this subtask.
  - dependencies: A list of dependencies (other subtask names) that need to be completed before this subtask can be executed.

Important: The generated JSON must strictly follow the JSON format. The following rules must be strictly adhered to:
1. All keys and values must be enclosed in double quotes.
2. All elements in arrays must be separated by commas.
3. All fields in the JSON must be complete and correctly formatted, with no missing or incorrect elements.

Your task is to generate the final plan in the specified JSON format, minimizing both the completion time and total cost. Do not provide any implementation code.

Here is an example to better understand the task:

{example}

Now, based on the following transformation rules, initial nodes, and target node, please provide an optimal plan that allows the target node to be obtained in the shortest time with the minimal total cost, supporting parallel transformations.
Only include necessary steps that are required for the fastest completion with the least cost. Do not add any extra or redundant transformation steps.
Task:
```json
{task}
```
"""

example = """
Task1:
```json
{
    "rules": [
        {
            "source": ["N1"],
            "target": ["N2"],
            "time": 3,
            "cost": 1
        },
        {
            "source": ["N6"],
            "target": ["N3"],
            "time": 4,
            "cost": 1
        },
        {
            "source": ["N2", "N3"],
            "target": ["N4"],
            "time": 2,
            "cost": 1
        },
        {
            "source": ["N4"],
            "target": ["N5"],
            "time": 1,
            "cost": 1
        },
        {
            "source": ["N2"],
            "target": ["N5"],
            "time": 5,
            cost": 1
        }
    ],
    "initial_source": ["N1", "N6"],
    "target": "N5"
}
```

Expected output:
```json
[
    {
      "name": "Subtask1",
      "source": ["N1"],
      "target": "N2",
      "dependencies": []
    },
    {
      "name": "Subtask2",
      "source": ["N6"],
      "target": "N3",
      "dependencies": []
    },
    {
      "name": "Subtask3",
      "source": ["N2", "N3"],
      "target": "N4",
      "dependencies": ["Subtask1", "Subtask2"]
    },
    {
      "name": "Subtask4",
      "source": ["N4"],
      "target": "N5",
      "dependencies": ["Subtask3"]
    }
]
```

Task2:
```json
{
    "rules": [
        {
            "source": ["Node_4355f195231e464da170f1d196c8bf71"],
            "target": ["Node_aa1433802c594c239e914be7f482059b"],
            "time": 25,
            "cost": 1
        },
        {
            "source": ["Node_aa1433802c594c239e914be7f482059b"],
            "target": ["Node_2a33b40427a34e7bacce09b869396cbe"],
            "time": 49,
            "cost": 1
        },
        {
            "source": ["Node_2a33b40427a34e7bacce09b869396cbe"],
            "target": ["Node_ec3fdb534d5f489baba1f61ff9718eac"],
            "time": 3,
            "cost": 1
        },
        {
            "source": ["Node_aa1433802c594c239e914be7f482059b"],
            "target": ["Node_44ed2b197fb94daaa89ae4a4e2f9f7cb"],
            "time": 45,
            "cost": 1
        },
        {
            "source": ["Node_4355f195231e464da170f1d196c8bf71"],
            "target": ["Node_62fb25e2d44e47efa0582f7d8b303e62"],
            "time": 48,
            "cost": 1
        },
        {
            "source": ["Node_4355f195231e464da170f1d196c8bf71"],
            "target": ["Node_1add136469184c70a10caa1650b80aca"],
            "time": 9,
            "cost": 1
        },
        {
            "source": ["Node_44ed2b197fb94daaa89ae4a4e2f9f7cb",
                "Node_1add136469184c70a10caa1650b80aca"],
            "target": ["Node_b560f21386fb41f689e780d6c8268f34"],
            "time": 28,
            "cost": 1
        },
        {
            "source": ["Node_4355f195231e464da170f1d196c8bf71"],
            "target": ["Node_f33f488cca4c443b8bbae2e215ce79c3"],
            "time": 20,
            "cost": 1
        }
    ],
    "initial_source": ["Node_4355f195231e464da170f1d196c8bf71"],
    "target": "Node_f33f488cca4c443b8bbae2e215ce79c3"
}
```

Expected output:
```json
[
    {
        "name": "Subtask1",
        "source": ["Node_4355f195231e464da170f1d196c8bf71"],
        "target": ["Node_f33f488cca4c443b8bbae2e215ce79c3"],
        "dependencies": []
    }
]
```
"""