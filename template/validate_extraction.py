"""Validation template for rule extraction verification."""

instruction = """
Task: Validate extracted structured transition rules against the original narrative.

Objective: Compare the extracted JSON rules with the original story to identify:
1. Missing rules (transitions mentioned in the story but not in the JSON)
2. Incorrect rules (rules in JSON that don't match the story)
3. Incorrect values (time, cost, source, target)

Input: 
- Original story describing a workflow
- Extracted rules in JSON format

Output: A JSON object with:
1. "is_valid": boolean (true if extraction is complete and accurate)
2. "confidence": float (0.0 to 1.0, how confident you are in the validation)
3. "issues": list of strings describing any problems found (empty if valid)
4. "suggestions": list of strings with corrections needed (empty if valid)
5. "corrected_rules": (optional) if issues found, provide corrected version of the JSON

Validation Criteria:
- All transitions mentioned in the story MUST be in the rules
- All rules MUST be supported by the story
- Time and cost values must be correct
- Source and target nodes must match exactly
- initial_source and target must be correct

Original Story:
{story}

Extracted Rules:
{extracted_json}

Please validate and provide feedback in the following JSON format:
```json
{{
    "is_valid": boolean,
    "confidence": float,
    "issues": ["list of issues"],
    "suggestions": ["list of suggestions"],
    "corrected_rules": null or {{"rules": [...], "initial_source": [...], "target": "..."}}
}}
```
"""

def get_validation_prompt(story: str, extracted_json: str) -> str:
    """Generate validation prompt with story and extracted JSON."""
    return instruction.format(story=story, extracted_json=extracted_json)
