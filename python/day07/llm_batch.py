import asyncio
async def call_llm(name,prompt):
    print("模型" + name +"开始处理："+prompt)
    await asyncio.sleep(2)
    print("已经处理模型：" + name + "\n已经处理提示词：" + prompt)
    return "已经处理模型：" + name + "\n已经处理提示词：" + prompt
async def main():
    task_a = asyncio.create_task(call_llm("deepseek","解释什么是 RAG"))
    task_b = asyncio.create_task(call_llm("gpt", "解释什么是 Agent"))
    task_c = asyncio.create_task(call_llm("deepseek", "解释什么是 Embedding"))
    result = await asyncio.gather(
        task_a,
        task_b,
        task_c
    )
    print(result)
asyncio.run(main())
