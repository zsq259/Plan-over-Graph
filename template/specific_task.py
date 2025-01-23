instruction = """
Transform this abstract task into a specific task in a real-world scenario, noting the following:
1. Tasks without dependencies can be executed in parallel.
2. Please express the instructions in complete natural language without explicitly listing the rules.
3. As long as there is one path that reaches the final goal, it is considered successful.
4. The source of a rule must be fully achieved before proceeding with the rule and obtaining its target.
5. You must strictly follow the rules I have given, make sure the rules in your story correspond one-to-one with the rules I have provided, and the sum of rules in your story must be equal to the sum of rules in the task.
6. You must explicitly mention both the time and cost associated with each rule in the story.
7. You only need to write the rules as a story, without offering any additional evaluation comments or introductory remarks.

Here is an example from another task for reference:

Input:
```json
{example}
```

OutPut:
In a busy urban construction project, multiple sites must be coordinated to build the "Core Area(N9)" as quickly and cost-effectively as possible. The project begins at three sites: "Infrastructure(N1)," "Elevated(N3)," and "Residential(N7)," each with different tasks. The "Infrastructure Area(N1)" takes 3 days and costs 1 to proceed to the "Bridge Area(N2)", while the "Elevated Area(N3)" moves to the "Building Area(N4)" in 3 days and at a cost of 1. The "Bridge Area(N2)" connects to the "Road Area(N5)" in 4 days and costs 1, and can directly connect to the "Facilities Area(N6)" in 8 days at a cost of 1. The "Building Area(N4)" partners with the "Road Area(N5)" to build the "Facilities Area(N6)" in 2 days and at a cost of 1. The "Residential Area(N7)" takes 5 days and costs 1 to reach the "City Center Area(N8)", while the "Building Area(N4)" directly reaches it in 1 day and costs 1. Once the "Facilities(N6)" and "City Center(N8)" areas are ready, they combine to complete the "Core Area(N9)" in 2 days at a cost of 1. The "Infrastructure Area(N1)" has a shortcut to bypass other areas and reach the "Core Area(N9)" in 15 days at a cost of 1. The project team can select the most efficient route based on resources and progress.

Input:
```json
{task}
```

Output:
"""

example_task = {"rules": [{ 'id': 0, "source": ["N1"], "target": ["N2"], "time": 3, "cost": 1 }, { 'id': 1, "source": ["N3"], "target": ["N4"], "time": 3, "cost": 1 }, { 'id': 2, "source": ["N2"], "target": ["N5"], "time": 4, "cost": 1 }, { 'id': 3, "source": ["N4", "N5"], "target": ["N6"], "time": 2, "cost": 1 }, { 'id': 4, "source": ["N2"], "target": ["N6"], "time": 8, "cost": 1 }, { 'id': 5, "source": ["N7"], "target": ["N8"], "time": 5, "cost": 1 }, { 'id': 6, "source": ["N4"], "target": ["N8"], "time": 1, "cost": 1 }, { 'id': 7, "source": ["N6", "N8"], "target": ["N9"], "time": 2, "cost": 1 }, { 'id': 8, "source": ["N1"], "target": ["N9"], "time": 15, "cost": 1 }, ], "initial_source": ["N1", "N3", "N7"], "target": "N9"}
