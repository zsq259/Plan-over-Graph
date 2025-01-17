instruction = """
Transform this abstract task into a specific task in a real-world scenario, noting the following:
1. Tasks without dependencies can be executed in parallel.
2. Please express the instructions in complete natural language without explicitly listing the rules.
3. As long as there is one path that reaches the final goal, it is considered successful.
4. The source of a rule must be fully achieved before proceeding with the rule and obtaining its target.
5. You must strictly follow the rules I have given, even if some of them are ineffective.
6. You only need to write the rules as a story, without offering any additional evaluation that could influence the solution.

{task}

Here is an example from another task for reference:

In a busy city construction project, multiple construction sites must be coordinated to build the "core area" as quickly and cost-effectively as possible. The project starts with three sites: "Infrastructure", "Overpass", and "Residential", each with different tasks. The "Infrastructure" site requires 3 days and 1 unit of cost to connect to the "Bridge Area"; meanwhile, the "Overpass Area" takes 3 days and 1 unit of cost to connect to the "Building Area." The "Bridge Area" can connect to the "Road Area" after 4 days and 1 unit of cost, or directly connect to the "Facilities Area" after 8 days and 1 unit of cost. The "Building Area", in collaboration with the "Road Area", can take 2 days and 1 unit of cost to construct the "Facilities Area". The "Residential Area" requires 5 days and 1 unit of cost to reach the "City Center Area", while the "Building Area" can directly connect to the "City Center Area" in just 1 day with a cost of 1. Once the "Facilities Area" and the "City Center Area" are ready, they will merge, requiring 2 days and 1 unit of cost to complete the "Core Area". The "Infrastructure Area" has a shortcut that bypasses other areas and directly reaches the "Core Area" after 15 days and 1 unit of cost. The project team can choose the most effective path based on resources and progress.
"""