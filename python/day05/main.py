from api_client import APIClient
client = APIClient("https://jsonplaceholder.typicode.com")
response=client.get("/posts/1")
if response is not None:
    print(response.json())
data={
    "title": "learn http",
    "body": "day5 practice",
    "userId": 1
}
response = client.post("/posts",json=data)
if response is not None:
    print(response.json())
    print(response.status_code)