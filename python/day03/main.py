from llm.qwen import QwenLLM
qwen = QwenLLM("qwen-plus")
try:
    ans = qwen.chat("")
except ValueError:
    print("调用失败")
else:
    print(ans)