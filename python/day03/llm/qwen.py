from .base import BaseLLM
class QwenLLM(BaseLLM):
    def chat(self,prompt):
        if prompt == "":
            raise ValueError("prompt 不能为空")
        return "Qwen response: " + prompt