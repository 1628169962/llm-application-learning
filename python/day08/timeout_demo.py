import asyncio
import httpx
url = "https://httpbin.org/delay/3"
async def request(url,timeout=0.1):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url,timeout=timeout)
    except httpx.TimeoutException:
        print("请求超时")
    else:
        print(response.status_code)
asyncio.run(request(url))