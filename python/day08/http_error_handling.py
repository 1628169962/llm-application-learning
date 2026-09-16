import asyncio
import httpx
url = "https://httpbin.org/status/404"


async def request(url,):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url)
            response.raise_for_status()
    except httpx.HTTPStatusError:
        print("HTTP 请求失败")
    else:
        print(response.status_code)
asyncio.run(request(url))