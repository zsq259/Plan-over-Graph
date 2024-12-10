instruction = """
You are given a set of transformation rules, where each rule consists of source nodes (materials or subtasks), target nodes (resulting materials or tasks), the time required to complete the transformation, and a cost associated with the transformation. Your goal is to write an algorithm that computes a plan from the initial nodes to the target node, supporting parallel transformations, such that the target node is obtained in the shortest time possible, while minimizing the total cost.
Input format:
- Transformation rules: A list of dictionaries, where each dictionary represents a transformation rule and contains:
  - source: A list of source nodes (the prerequisites for the transformation).
  - target: A list of target nodes (the result of the transformation).
  - time: The time required to complete the transformation (an integer).
  - cost: The cost associated with the transformation (an integer).

- Initial nodes: A list of strings representing the available nodes at the start.

- Target node: A string representing the node that needs to be obtained.

Output format:
- The algorithm should output a list of subtasks, where each subtask is represented as a JSON object with the following fields:
  - name: The name of the subtask or node being completed. The default name format is "Subtask" followed by a sequence number.
  - source: A list of source nodes involved in this subtask. The sources must be products you already have or can obtain through previous steps.
  - target: The target node resulting from this subtask. Both the source and target must conform to a given rule and cannot be assumed or self-created.
  - dependencies: A list of dependencies (other subtask names) that need to be completed before this subtask can be executed. This ensures the execution order between subtasks, and the dependencies must provide the required sources for this subtask.

Important:
- The algorithm should minimize both the completion time and total cost.
- All steps must comply with the given transformation rules.
- All substances and steps must conform to the rules and the initial nodes provided.
- The algorithm should utilize parallel transformations wherever possible to speed up the process.
Your task is to write an algorithm (in any language of your choice) that solves this task. The algorithm should compute the final plan, ensuring that the target node is obtained in the shortest time possible while minimizing total cost, and it should support parallel transformations. You should not just provide the output plan, but the algorithm that generates the plan.
Here is an example to better understand the task:

{example}

Now, based on the following transformation rules, initial nodes, and target node, write an algorithm that computes the optimal plan that allows the target node to be obtained in the shortest time with the minimal total cost, supporting parallel transformations. Only include the steps necessary for the fastest completion with the least cost. Do not include any extra or redundant steps.
Do not provide the final output JSON directly. Instead, provide the implementation of the algorithm that generates the output based on the input data.
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