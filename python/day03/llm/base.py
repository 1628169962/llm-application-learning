class BaseLLM:
    def __init__(self,model):
        self.model=model
    def chat(self,prompt):
        return  "base response"