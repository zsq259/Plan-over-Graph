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
Let's think step by step and then output the final solution in JSON format.

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
Example Task:
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

Example Output:
**Think Step by Step:**  
To determine the optimal plan, we analyze dependencies and parallelization opportunities:  
1. **Initial Parallelization**:  
   - (N3→N4, 3 days) and (N1→N2, 3 days) can start immediately and run in parallel since they have no dependencies.  
   - (N7→N8, 5 days) is also independent and starts concurrently.  

2. **Sequential Dependencies**:  
   - (N2→N5, 4 days) requires (N1→N2, 3 days) to finish first. Thus, it starts after 3 days and completes at **7 days**.  
   - (N4+N5→N6, 2 days) depends on (N3→N4, 3 days) and (N2→N5, 7 days). It begins at **7 days** and ends at **9 days**.  
   - (N4→N8, 1 day) depends on (N3→N4, 3 days). It starts at **3 days** and finishes at **4 days**.  

3. **Critical Path Analysis**:  
   - The path (N1→N2, 3 days) → (N2→N5, 4 days) → (N4+N5→N6, 2 days) takes **3 + 4 + 2 = 9 days**.  
   - The path (N3→N4, 3 days) → (N4→N8, 1 days) takes **3 + 1 = 4 days**.  
   - (N6+N8→N9, 2 days) requires both (N4+N5→N6) (9 days) and (N4→N8) (4 days). It starts at **9 days** and ends at **11 days**.  

4. **Avoiding the Shortcut**:  
   - The alternative shortcut (N1→N9, 15 days) is slower than the critical path (11 days), so it's excluded.  

**Conclusion**:  
The longest path (critical path) determines the total time: (N1→N2, 3 days) → (N2→N5, 4 days) → (N4+N5→N6, 2 days) → (N6+N8→N9, 2 days) takes (3 + 4 + 2 + 2 = **11 days**). Parallel execution of independent tasks minimizes cost while achieving the shortest time.  

```json
[
    {
        "name": "Subtask1",
        "source": [
            "N3"
        ],
        "target": [
            "N4"
        ],
        "dependencies": []
    },
    {
        "name": "Subtask2",
        "source": [
            "N1"
        ],
        "target": [
            "N2"
        ],
        "dependencies": []
    },
    {
        "name": "Subtask3",
        "source": [
            "N2"
        ],
        "target": [
            "N5"
        ],
        "dependencies": [
            "Subtask2"
        ]
    },
    {
        "name": "Subtask4",
        "source": [
            "N4",
            "N5"
        ],
        "target": [
            "N6"
        ],
        "dependencies": [
            "Subtask1",
            "Subtask3"
        ]
    },
    {
        "name": "Subtask5",
        "source": [
            "N4"
        ],
        "target": [
            "N8"
        ],
        "dependencies": [
            "Subtask1"
        ]
    },
    {
        "name": "Subtask6",
        "source": [
            "N6",
            "N8"
        ],
        "target": [
            "N9"
        ],
        "dependencies": [
            "Subtask4",
            "Subtask5"
        ]
    }
]
```
"""