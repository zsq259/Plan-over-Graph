class Excutor:
    def __init__(self, env):
        self.env = env
        self.name = 'Excutor'

    def run(self, action):
        return self.env.step(action)
    
class HotPotQAExcutor(Excutor):
    def __init__(self, env):
        super().__init__(env)
        self.name = 'HotPotQAExcutor'
        
    def run(self, action):
        return self.env.step(action)