class SubTaskNode:
    def __init__(self, subtask: dict):
        self.name = subtask['name']
        self.description = subtask['description']
        self.dependencies = subtask['dependencies']
        self.infos = []
        self.answer = ''