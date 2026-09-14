import asyncio
# async def hello():
#     print("hello async")
#
# asyncio.run(hello())

async def request(name):
    print(name + " 开始请求")
    await asyncio.sleep(2)
    print(name + " 请求完成")
    return name + " 的返回结果"
async def main():
    task_a = asyncio.create_task(request("A"))
    task_b = asyncio.create_task(request("B"))
    task_c = asyncio.create_task(request("C"))
    results = await asyncio.gather(
        task_a,
        task_b,
        task_c
    )
    print(results)
asyncio.run(main())