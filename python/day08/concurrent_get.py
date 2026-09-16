import asyncio
import httpx
import time
urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2"
]
async def request(client, url):
    response = await client.get(url)
    return response.status_code

async def main(urls):
    async with httpx.AsyncClient() as client:
        task_a = request(client, urls[0])
        task_b = request(client, urls[1])
        task_c = request(client, urls[2])
        start = time.perf_counter()
        result = await asyncio.gather(
            task_a,
            task_b,
            task_c
        )
        end = time.perf_counter()
        ans = end -start
        print(result,ans)
asyncio.run(main(urls))

