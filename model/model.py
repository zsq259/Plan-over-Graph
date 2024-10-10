import json
import re

class Model:
    def __init__(self, name=None):
        self.name = name
        
    def predict(self, stop=None):
        raise NotImplementedError   
        
    
    