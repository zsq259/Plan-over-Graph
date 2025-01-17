intstuction = """
{task}
Projects without dependencies can be completed in parallel to improve overall efficiency. Now, please provide a plan to minimize costs while minimizing completion time.

Please provide the final solution in JSON format:
- Plan: A list of subtasks, where each subtask is a JSON object with the following fields:
  - name: The name of the subtask or node being completed. The default name format is "Subtask" followed by a sequence number.
  - source: A list of source nodes involved in this subtask. The sources must be products you already have or can obtain through previous steps.
  - target: The target node resulting from this subtask. Both the source and target must conform to a given rule and cannot be assumed or self-created.
  - dependencies: A list of dependencies (other subtask names) that need to be completed before this subtask can be executed. This ensures the execution order between subtasks, and the dependencies must provide the required sources for this subtask.
Here is an example:
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
      "target": ["N3"],
      "dependencies": ["Subtask1"]
    }
]
```
"""