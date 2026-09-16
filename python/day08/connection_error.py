import asyncio
import httpx
url = "http://this-domain-should-not-exist.invalid"
async def request(url):
    try:
        async with httpx.AsyncClient(trust_env=False) as client:
            await client.get(url)
    except httpx.RequestError:
        print("网络请求失败")
asyncio.run(request(url))