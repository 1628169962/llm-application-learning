import asyncio
import httpx
urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/200"
]
async def request(client,url):
    try:
        response = await client.get(url)
        response.raise_for_status()
    except httpx.HTTPStatusError:
        print("HTTP 请求失败")
        return "failed"
    except httpx.TimeoutException:
        print("请求超时")
        return "failed"
    else:
        return "success"

async def main(urls):
    async with httpx.AsyncClient() as client:
        task_1 = request(client,urls[0])
        task_2 = request(client,urls[1])
        task_3 = request(client,urls[2])
        result = await asyncio.gather(
            task_1,
            task_2,
            task_3
        )
        print(result)
asyncio.run(main(urls))
