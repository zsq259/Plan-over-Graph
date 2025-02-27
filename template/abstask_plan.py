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
  - name: The name of the subtask or node being completed. The default name format is "Subtask" followed by a sequence number.
  - source: A list of source nodes involved in this subtask. The sources must be products you already have or can obtain through previous steps.
  - target: The target node resulting from this subtask. Both the source and target must conform to a given rule and cannot be assumed or self-created.
  - dependencies: A list of dependencies (other subtask names) that need to be completed before this subtask can be executed. This ensures the execution order between subtasks, and the dependencies must provide the required sources for this subtask.

Important: 
- The generated JSON must strictly follow the JSON format. The following rules must be strictly adhered to:
  - All keys and values must be enclosed in double quotes.
  - All elements in arrays must be separated by commas.
  - All fields in the JSON must be complete and correctly formatted, with no missing or incorrect elements.
- All planned steps must comply with a given rule.
- All substances involved must conform to the given rules.

Your task is to generate the final plan in the specified JSON format, minimizing both the completion time and total cost. Do not provide any implementation code.

Here is an example to better understand the task:

{example}

Now, based on the following transformation rules, initial nodes, and target node, please provide an optimal plan that allows the target node to be obtained in the shortest time with the minimal total cost, supporting parallel transformations.
Only include necessary steps that are required for the fastest completion with the least cost. Do not add any extra or redundant transformation steps.
Task:
```json
{task}
```

Your task is to generate the final plan in the specified JSON format. Do not provide any implementation code.

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
      "target": ["N2"],
      "dependencies": []
    },
    {
      "name": "Subtask2",
      "source": ["N6"],
      "target": ["N3"],
      "dependencies": []
    },
    {
      "name": "Subtask3",
      "source": ["N2", "N3"],
      "target": ["N4"],
      "dependencies": ["Subtask1", "Subtask2"]
    },
    {
      "name": "Subtask4",
      "source": ["N4"],
      "target": ["N5"],
      "dependencies": ["Subtask3"]
    }
]
```

Task2:
```json
{
    "rules": [
        {
            "source": ["N1"],
            "target": ["N2"],
            "time": 12,
            "cost": 1
        },
        {
            "source": ["N1","N2"],
            "target": ["N3"],
            "time": 28,
            "cost": 1
        },
        {
            "source": ["N2","N1"],
            "target": ["N4"],
            "time": 3,
            "cost": 1
        },
        {
            "source": ["N3"],
            "target": ["N4"],
            "time": 14,
            "cost": 1
        },
        {
            "source": ["N1","N4"],
            "target": ["N5"],
            "time": 12,
            "cost": 1
        },
        {
            "source": ["N2","N5","N3"],
            "target": ["N6"],
            "time": 18,
            "cost": 1
        },
        {
            "source": ["N3","N6"],
            "target": ["N7"],
            "time": 49,
            "cost": 1
        },
        {
            "source": ["N2","N5"],
            "target": ["N7"],
            "time": 39,
            "cost": 1
        },
        {
            "source": ["N7"],
            "target": ["N8"],
            "time": 49,
            "cost": 1
        },
        {
            "source": ["N5"],
            "target": ["N8"],
            "time": 34,
            "cost": 1
        },
        {
            "source": ["N1"],
            "target": ["N8"],
            "time": 42,
            "cost": 1
        },
        {
            "source": ["N2"],
            "target": ["N8"],
            "time": 20,
            "cost": 1
        },
        {
            "source": ["N1","N7"],
            "target": ["N9"],
            "time": 34,
            "cost": 1
        },
        {
            "source": ["N4","N3"],
            "target": ["N9"],
            "time": 24,
            "cost": 1
        }
    ],
    "initial_source": ["N1"],
    "target": "N8"
}
```

Expected output:
```json
[
    {
        "name": "Subtask1",
        "source": ["N1"],
        "target": ["N2"],
        "dependencies": []
    },
    {
        "name": "Subtask2",
        "source": ["N2"],
        "target": ["N8"],
        "dependencies": [
            "Subtask1"
        ]
    }
]
```
"""

example1 = """
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
            "source": ["N3"],
            "target": ["N4"],
            "time": 3,
            "cost": 1
        },
        {
            "source": ["N2"],
            "target": ["N5"],
            "time": 4,
            "cost": 1
        },
        {
            "source": ["N4", "N5"],
            "target": ["N6"],
            "time": 2,
            "cost": 1
        },
        {
            "source": ["N2"],
            "target": ["N6"],
            "time": 8,
            "cost": 1
        },
        {
            "source": ["N7"],
            "target": ["N8"],
            "time": 5,
            "cost": 1
        },
        {
            "source": ["N4"],
            "target": ["N8"],
            "time": 1,
            "cost": 1
        },
        {
            "source": ["N6", "N8"],
            "target": ["N9"],
            "time": 2,
            "cost": 1
        },
        {
            "source": ["N1"],
            "target": ["N9"],
            "time": 15,
            "cost": 1
        },
    ],
    "initial_source": ["N1", "N3", "N7"],
    "target": "N9"
}
```
"""