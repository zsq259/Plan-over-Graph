instruction = """
You are given a set of transformation rules, where each rule consists of source nodes (materials or subtasks), target nodes (resulting materials or tasks), and the time required to complete the transformation. Your goal is to plan a path from the initial nodes to the target node, supporting parallel transformations, to obtain the target node in the shortest time possible.
Input format:
- Transformation rules: A list of dictionaries, where each dictionary represents a transformation rule and contains:
  - source: A list of source nodes (the prerequisites for the transformation).
  - target: A list of target nodes (the result of the transformation).
  - time: The time required to complete the transformation (an integer).

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
Your task is to generate the final plan in the specified JSON format. Do not provide any implementation code.

here is a example for you to understand the task better:

{example}

Now, based on the following transformation rules, initial nodes, and target node, please provide an optimal plan that allows the target node to be obtained in the shortest time, supporting parallel transformations.
Only include necessary steps that are required for the fastest completion. Do not add any extra or redundant transformation steps.

```json
{task}
```

Your task is to generate the final plan in the specified JSON format. Do not provide any implementation code.

"""

example = """
```json
{
    "rules": [
        {
            "source": ["N1"],
            "target": ["N2"],
            "time": 3
        },
        {
            "source": ["N6"],
            "target": ["N3"],
            "time": 4
        },
        {
            "source": ["N2", "N3"],
            "target": ["N4"],
            "time": 2
        },
        {
            "source": ["N4"],
            "target": ["N5"],
            "time": 1
        },
        {
            "source": ["N2"],
            "target": ["N5"],
            "time": 5
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
"""