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

Example Input Story:  
"A hospital designs a patient workflow starting at 'Admission(N1)'. From N1:  
- Proceed to 'Triage(N2)' in 2 days (cost=1).  
- If both N1 and N2 are complete, begin 'Diagnostics(N3)' in 3 days (cost=1).  
A shortcut allows moving from N2 directly to 'Discharge(N4)' in 1 day (cost=1). The final phase 'Billing(N5)' requires N3 and N4, taking 5 days (cost=1)."  

Example Output:
```json
{example}
```

Your Task: Convert the following story into the JSON format above. Ensure:  
1. All transitions are captured, including multi-source dependencies and shortcuts  
2. Node IDs (e.g., N1, N2) are preserved exactly as written  
3. Time and cost values are strictly numeric  
4. Follow the JSON schema precisely  

Input Story:
{task}

Output:
"""

example = {
  "rules": [
    {"id": 0, "source": ["N1"], "target": ["N2"], "time": 2, "cost": 1},
    {"id": 1, "source": ["N1", "N2"], "target": ["N3"], "time": 3, "cost": 1},
    {"id": 2, "source": ["N2"], "target": ["N4"], "time": 1, "cost": 1},
    {"id": 3, "source": ["N3", "N4"], "target": ["N5"], "time": 5, "cost": 1}
  ],
  "initial_source": ["N1"],
  "target": "N5"
}