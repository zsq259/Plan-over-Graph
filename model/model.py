import json
import re

class Model:
    def __init__(self, name=None):
        self.name = name
        
    def predict(self):
        raise NotImplementedError
    
    def step(self):
        raise NotImplementedError
    
    def get_actions(self, content=None):
        match = re.search(r'^(.*)\nActions? \d+:\s*(\[[\'"].*[\'"]\])', content, re.DOTALL)
        if match:
            thought = match.group(1).strip()
            actions = match.group(2).strip()
            actions = actions.replace("'", '"')
            return thought, actions
        else:
            raise ValueError("Thought Actions No match: {}".format(content))
    
    def find_actions(self, actions: str) -> list:
        print(actions)
        return json.loads(actions)
    

if __name__ == "__main__":
    content = """From the observations, I have found that Der Rosenkavalier and I Capuleti e i Montecchi are opera adaptations of different plays, with Der Rosenkavalier having a comic element. I now need to confirm if I Capuleti e i Montecchi is also a comic opera or not.
Action 2: ['Search[I Capuleti e i Montecchi]']    
    """
    model = Model(name="test")
    thought, actions = model.get_actions(content)
    print(thought)
    print(actions)
    print(model.find_actions(actions))        
        
    
    