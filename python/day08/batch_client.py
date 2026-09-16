from async_client import AsyncAPIClient
import asyncio
async def main():
    client = AsyncAPIClient(base_url = "https://httpbin.org",timeout=5)
    task_1 = client.get("/get")
    task_2 = client.get("/status/404")
    task_3 = client.get("/json")
    results = await asyncio.gather(
        task_1,
        task_2,
        task_3
    )
    print(results)
    success_results = []
    failed_results = []
    for x in results:
        if x["code_status"] == "success":
            success_results.append(x)
        else:
            failed_results.append(x)
    print(f"成功数量：{len(success_results)}")
    print(f"失败数量：{len(failed_results)}")
    print(success_results)
    print(failed_results)

asyncio.run(main())