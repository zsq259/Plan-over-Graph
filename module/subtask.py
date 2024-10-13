class SubTaskNode:
    def __init__(self):
        self.name = ''
        self.dependencies = []

class SubQANode:
    def __init__(self, subtask: dict):
        self.name = subtask['name']
        self.question = subtask['question']
        self.description = subtask['description'] if 'description' in subtask else ''
        self.dependencies = subtask['dependencies']
        self.infos = []
        self.answer = ''
    def update_info(self, info):
        self.infos.append(info)