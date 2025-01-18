instruction = """
For the input task, please provide an optimal plan that allows the target to be obtained. 
Minimize the cost under the premise of the shortest time.
Projects without dependencies can be completed in parallel to improve overall efficiency. 


Please provide the final solution in JSON format:
- Plan: A list of subtasks, where each subtask is a JSON object with the following fields:
  - name: The name of the subtask or node being completed. The default name format is "Subtask" followed by a sequence number.
  - source: A list of source nodes involved in this subtask. The sources must be products you already have or can obtain through previous steps.
  - target: The target node resulting from this subtask. Both the source and target must conform to a given rule and cannot be assumed or self-created.
  - dependencies: A list of dependencies (other subtask names) that need to be completed before this subtask can be executed. This ensures the execution order between subtasks, and the dependencies must provide the required sources for this subtask.
Here is an example:

Input:
In a busy urban construction project, multiple sites must be coordinated to build the "Core Area(N9)" as quickly and cost-effectively as possible. The project begins at three sites: "Infrastructure(N1)," "Elevated(N3)," and "Residential(N7)," each with different tasks. The "Infrastructure Area(N1)" takes 3 days and costs 1 to proceed to the "Bridge Area(N2)", while the "Elevated Area(N3)" moves to the "Building Area(N4)" in 3 days and at a cost of 1. The "Bridge Area(N2)" connects to the "Road Area(N5)" in 4 days and costs 1, and can directly connect to the "Facilities Area(N6)" in 8 days at a cost of 1. The "Building Area(N4)" partners with the "Road Area(N5)" to build the "Facilities Area(N6)" in 2 days and at a cost of 1. The "Residential Area(N7)" takes 5 days and costs 1 to reach the "City Center Area(N8)", while the "Building Area(N4)" directly reaches it in 1 day and costs 1. Once the "Facilities(N6)" and "City Center(N8)" areas are ready, they combine to complete the "Core Area(N9)" in 2 days at a cost of 1. The "Infrastructure Area(N1)" has a shortcut to bypass other areas and reach the "Core Area(N9)" in 15 days at a cost of 1. The project team can select the most efficient route based on resources and progress.

Output:
```json
{example_output}
```

Input:
{story_task}

Output:
```
"""

example_output = [{'name': 'Subtask1', 'source': ['N3'], 'target': ['N4'], 'dependencies': []}, {'name': 'Subtask2', 'source': ['N1'], 'target': ['N2'], 'dependencies': []}, {'name': 'Subtask3', 'source': ['N2'], 'target': ['N5'], 'dependencies': ['Subtask2']}, {'name': 'Subtask4', 'source': ['N4', 'N5'], 'target': ['N6'], 'dependencies': ['Subtask1', 'Subtask3']}, {'name': 'Subtask5', 'source': ['N4'], 'target': ['N8'], 'dependencies': ['Subtask1']}, {'name': 'Subtask6', 'source': ['N6', 'N8'], 'target': ['N9'], 'dependencies': ['Subtask4', 'Subtask5']}]