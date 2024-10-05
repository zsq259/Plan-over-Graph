class SubTaskNode:
    def __init__(self, subtask: dict):
        self.name = subtask['name']
        self.question = subtask['question']
        self.description = subtask['description'] if 'description' in subtask else ''
        self.dependencies = subtask['dependencies']
        self.infos = []
        self.answer = ''