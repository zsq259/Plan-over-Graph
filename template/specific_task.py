intstuction = """
{story_task}
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

example_task = """
In a large-scale event planning scenario, the goal is to successfully organize a grand festival, with the final objective being the "Grand Finale" (N10). The planning begins with three initial tasks: "Venue Setup" (N1), "Entertainment Booking" (N2), and "Vendor Coordination" (N5). Each of these tasks has its own dependencies and timelines.

The "Entertainment Booking" (N2) team can proceed to secure the "Stage Design" (N3) in 33 days with a cost of 1 unit. Alternatively, the "Venue Setup" (N1) team can also work on the "Stage Design" (N3) but will take 40 days with the same cost. Meanwhile, the "Entertainment Booking" (N2) team can also move forward to arrange the "Lighting and Sound" (N4) in 45 days, costing 1 unit.

The "Venue Setup" (N1) team has another responsibility: they need to prepare the "Guest Accommodation" (N6), which will take 41 days and cost 1 unit. Simultaneously, the "Vendor Coordination" (N5) team can also contribute to the "Guest Accommodation" (N6) by completing their part in 26 days with a cost of 1 unit. Additionally, once the "Lighting and Sound" (N4) is ready, it can be integrated into the "Guest Accommodation" (N6) in 39 days, costing 1 unit.

Once the "Stage Design" (N3), "Entertainment Booking" (N2), and "Guest Accommodation" (N6) are all completed, the team can move forward to organize the "Main Event" (N7), which will take 47 days and cost 1 unit. After the "Main Event" (N7) is successfully executed, the team can proceed to the "Post-Event Cleanup" (N8) in just 7 days with a cost of 1 unit. Alternatively, the "Venue Setup" (N1) team can directly handle the "Post-Event Cleanup" (N8) in 30 days with a cost of 1 unit.

Once both the "Post-Event Cleanup" (N8) and "Lighting and Sound" (N4) are completed, the team can work on the "Final Review and Feedback" (N9), which will take 43 days and cost 1 unit. After the "Final Review and Feedback" (N9) is done, the team can finally achieve the "Grand Finale" (N10) in 47 days with a cost of 1 unit. Alternatively, the "Entertainment Booking" (N2) team can directly contribute to the "Grand Finale" (N10) in 50 days with a cost of 1 unit.

The event planning team can choose the most efficient path based on the progress and resources available, ensuring that the "Grand Finale" (N10) is achieved successfully.
"""