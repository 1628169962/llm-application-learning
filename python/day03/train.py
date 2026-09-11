class BaseLLM:
    def chat(self, prompt):
        return "BaseLLM response"
class QwenLLM(BaseLLM):
    def chat(self, prompt):
        return "Qwen response"
qwen = QwenLLM()
print(qwen.chat("hello"))

