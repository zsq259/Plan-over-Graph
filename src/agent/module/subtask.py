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
        
class SubTTNode:
    def __init__(self, subtask: dict):
        self.name = subtask['name']
        self.source = subtask['source'] if 'source' in subtask else None
        self.target = subtask['target'] if 'target' in subtask else None
        self.perform_rule_indx = subtask['perform_rule_indx'] if 'perform_rule_indx' in subtask else None
        self.dependencies = subtask['dependencies']
        self.time = subtask['time'] if 'time' in subtask else 0
        self.cost = subtask['cost'] if 'cost' in subtask else 0
        
        if isinstance(self.source, str):
            self.source = [self.source]
        if isinstance(self.target, str):
            self.target = [self.target]