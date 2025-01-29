instruction = """
Task: Extract structured transition rules from unstructured workflow narratives.  
Objective: Identify all transitions between nodes in the text. For each transition, extract:  
- Source nodes (prerequisites)  
- Target nodes (outcomes)  
- Time (duration)  
- Cost (numeric resource units)  
Additionally, determine the initial_source (starting node) and target (final node).  

Input: A story describing a workflow process. Example phrases may include:  
- "From [NodeA], proceed to [NodeB] in X days at a cost of Y units"  
- "When both [NodeA] and [NodeB] are ready, start [NodeC]"  
- Shortcuts like "directly from [NodeA] to [NodeC] in Z days"  

Output: A JSON object with:  
1. "rules": A list of transition rules, each containing:  
   - "id" (sequential integer starting from 0)  
   - "source" (list of node IDs, e.g., ["N1"])  
   - "target" (list of node IDs, e.g., ["N2"])  
   - "time" (numeric value)  
   - "cost" (numeric value)  
2. "initial_source": List of starting node IDs (e.g., ["N1"])  
3. "target": Final node ID (e.g., "N8")  

Your Task: Convert the following story into the JSON format above. Ensure:  
1. All transitions are captured, including multi-source dependencies and shortcuts  
2. Node IDs (e.g., N1, N2) are preserved exactly as written  
3. Time and cost values are strictly numeric  
4. Follow the JSON schema precisely  

Example Input Story:  
In a busy urban construction project, multiple sites must be coordinated to build the "Core Area(N9)" as quickly and cost-effectively as possible. The project begins at three sites: "Infrastructure(N1)," "Elevated(N3)," and "Residential(N7)," each with different tasks. The "Infrastructure Area(N1)" takes 3 days and costs 1 to proceed to the "Bridge Area(N2)", while the "Elevated Area(N3)" moves to the "Building Area(N4)" in 3 days and at a cost of 1. The "Bridge Area(N2)" connects to the "Road Area(N5)" in 4 days and costs 1, and can directly connect to the "Facilities Area(N6)" in 8 days at a cost of 1. The "Building Area(N4)" partners with the "Road Area(N5)" to build the "Facilities Area(N6)" in 2 days and at a cost of 1. The "Residential Area(N7)" takes 5 days and costs 1 to reach the "City Center Area(N8)", while the "Building Area(N4)" directly reaches it in 1 day and costs 1. Once the "Facilities(N6)" and "City Center(N8)" areas are ready, they combine to complete the "Core Area(N9)" in 2 days at a cost of 1. The "Infrastructure Area(N1)" has a shortcut to bypass other areas and reach the "Core Area(N9)" in 15 days at a cost of 1. The project team can select the most efficient route based on resources and progress.

Example Output:
```json
{example}
```

Input Story:
{task}

Output:
"""

example = {"rules": [{ 'id': 0, "source": ["N1"], "target": ["N2"], "time": 3, "cost": 1 }, { 'id': 1, "source": ["N3"], "target": ["N4"], "time": 3, "cost": 1 }, { 'id': 2, "source": ["N2"], "target": ["N5"], "time": 4, "cost": 1 }, { 'id': 3, "source": ["N4", "N5"], "target": ["N6"], "time": 2, "cost": 1 }, { 'id': 4, "source": ["N2"], "target": ["N6"], "time": 8, "cost": 1 }, { 'id': 5, "source": ["N7"], "target": ["N8"], "time": 5, "cost": 1 }, { 'id': 6, "source": ["N4"], "target": ["N8"], "time": 1, "cost": 1 }, { 'id': 7, "source": ["N6", "N8"], "target": ["N9"], "time": 2, "cost": 1 }, { 'id': 8, "source": ["N1"], "target": ["N9"], "time": 15, "cost": 1 }, ], "initial_source": ["N1", "N3", "N7"], "target": "N9"}