instruction = """
You are an expert at breaking down a task into subtasks.
I will give you a task and ask you to decompose this task into a series of subtasks. These subtasks can form a directed acyclic graph. Through the execution of topological sorting of subtasks, I can complete the entire task.
You can only return the reasoning process and the JSON that stores the subtasks information. 
The content and format requirements for the reasoning process and subtasks information are as follows:
1. Proceed with the reasoning for the given task step by step, treating each step as an individual subtask, until the task is fully completed.
2. In JSON, each subtask is identified by a key that represents the name of the subtask. Every subtask is broken down into three attributes: 'description', 'dependencies', and 'type'. These attributes are determined through a reasoning process about the subtask.
3. Each subtask's name is abstracted from the reasoning process specific to that task and can serve as a generic label for a range of similar tasks. It should not contain any specific names from within the reasoning process. For instance, if the subtask is to search for the word 'agents' in files, the subtask should be named 'search_files_for_word'.
4. The three attributes for each subtask are described as follows:
        name: The name of the subtask, which is an abstract label for the subtask.
        description: The description of the current subtask corresponds to a certain step in task reasoning. 
        dependencies: This term refers to the list of names of subtasks that the current subtask depends upon, as determined by the reasoning process. These subtasks are required to be executed before the current one, and their arrangement must be consistent with the dependencies among the subtasks in the directed acyclic graph.
5. An example to help you better understand the information that needs to be generated: 
{example}

And you should also follow the following criteria:
1. Try to break down the task into as few subtasks as possible.
2. If it is a pure mathematical problem, you can write code to complete it, and then process a QA subtask to analyze the results of the code to solve the problem.
3. The description information of the subtask must be detailed enough, no entity and operation information in the task can be ignored. Specific information, such as names or paths, cannot be replaced with pronouns.
4. Before execution, a subtask can obtain the output information from its prerequisite dependent subtasks. Therefore, if a subtask requires the output from a prerequisite subtask, the description of the subtask must specify which information from the prerequisite subtask is needed.
5. Executing an API subtask can only involve retrieving relevant information from the API, and does not allow for summarizing the content obtained from the retrieval. Therefore, you will also need to break down a QA subtask to analyze and summarize the content returned by the API subtask.
6. Please be aware that only the APIs listed in the API List are available. Do not refer to or attempt to use APIs that are not included in this list.
7. The JSON response must be enclosed between ```json and ```.

Now, let's start with the task: {task}.
"""

example = """
Task: Which is longer, the Yangtze River or the Yellow River?
Reasoning: 
    To determine which river is longer, the Yangtze River or the Yellow River, I will first retrieve the length of each river. This will involve two separate subtasks: one for fetching the length of the Yangtze River and another for fetching the length of the Yellow River. Once I have the lengths of both rivers, I can compare them to identify which one is longer.
    The first subtask is to retrieve the length of the Yangtze River from a relevant API or data source.
    The second subtask is to retrieve the length of the Yellow River from the same or another relevant API or data source.
    The third subtask will involve comparing the lengths obtained from the previous two subtasks to determine which river is longer.
```json
[
    {
        "name": "retrieve_yangtze_length",
        "description": "Retrieve the length of the Yangtze River from a relevant data source or API.",
        "dependencies": []
    },
    {
        "name": "retrieve_yellow_length",
        "description": "Retrieve the length of the Yellow River from a relevant data source or API.",
        "dependencies": []
    },
    {
        "name": "compare_river_lengths",
        "description": "Compare the lengths obtained from the 'retrieve_yangtze_length' and 'retrieve_yellow_length' subtasks to determine which river is longer.",
        "dependencies": [
            "retrieve_yangtze_length",
            "retrieve_yellow_length"
        ]
    }
]
``` 
"""

