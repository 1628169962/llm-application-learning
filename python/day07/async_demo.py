import asyncio
import time
async def task(name):
    print(name + " 开始请求")
    await asyncio.sleep(2)
    print(name + " 请求完成")

async def main():

    task_a = asyncio.create_task(task("A"))
    task_b = asyncio.create_task(task("B"))
    task_c = asyncio.create_task(task("C"))
    await asyncio.gather(
        task_a,
        task_b,
        task_c
    )

start = time.perf_counter()
asyncio.run(main())
end = time.perf_counter()
ans = end - start
print(ans)

