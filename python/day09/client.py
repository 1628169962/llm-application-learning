import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(trust_env=False) as client:
        task_1 = client.get("http://127.0.0.1:8000/health")
        task_2 = client.post("http://127.0.0.1:8000/chat",json={"message": "什么是 RAG？"})
        task_3 = client.post("http://127.0.0.1:8000/embedding",json={"text": "RAG 是什么"})
        result =await asyncio.gather(
            task_1,
            task_2,
            task_3
        )
        # response_1 = result[0].json()
        # response_2 = result[1].json()
        # response_3 = result[2].json()
        # print(response_1)
        # print(response_2)
        # print(response_3)
        print(result[2].status_code)
        print(repr(result[2].text))
asyncio.run(main())