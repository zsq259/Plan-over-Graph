class ExecEnv:
    def __init__(self):
        self.name = "ExecEnv"
        
    def run_action(self, action):
        raise NotImplementedError
    
    def run_actions(self, actions):
        for action in actions:
            self.run_action(action)
    
    def step(self, action):
        raise NotImplementedError