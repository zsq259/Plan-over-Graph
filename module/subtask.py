class SubTaskNode:
    def __init__(self, subtask: dict):
        self.name = subtask['name']
        self.question = subtask['question']
        self.dependencies = subtask['dependencies']
        self.infos = []
        self.answer = ''