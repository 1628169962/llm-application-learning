import asyncio
import httpx
dect={
    "model":"deepseek",
    "prompt":"hello"
}
url = "https://httpbin.org/post"
headers = {
    "Content-Type": "application/json"
}
async def request(url,dect,headers,timeout=5):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url,json=dect,headers=headers,timeout=timeout)
        print(response.status_code)
        print(response.json())
asyncio.run(request(url,dect,headers))