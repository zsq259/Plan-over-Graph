class Excutor:
    def __init__(self, env):
        self.env = env
        self.name = 'Excutor'

    def run(self, action):
        return self.env.step(action)