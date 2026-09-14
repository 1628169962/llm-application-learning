import requests
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
print(response.url)
print(response.status_code)
print(type(response.text))
data = response.json()
print(data)
print(type(data))
print(data["title"])
print(response.headers)
print(response.headers["Content-Type"])



import requests
params = {
    "postId": 1
}
url = "https://jsonplaceholder.typicode.com/comments"
response = requests.get(url,params)
print(response.url)

data = {
    "title": "learn http",
    "body": "day5 practice",
    "userId": 1
}
url = "https://jsonplaceholder.typicode.com/posts"
headers = {
    "X-Client-Name": "llm-intern"
}
response = requests.post(url,json=data,headers=headers,timeout=5)
print(response.status_code)
print(response.json())

url="https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url,timeout=5)
print(response.status_code)
print(response.json())

url = "https://jsonplaceholder.typicode.com/posts"
data={
    "title": "day5",
    "body": "http practice",
    "userId": 1
}
response = requests.post(url,json=data,timeout=5)
print(response.status_code)
print(response.json())

url ="https://jsonplaceholder.typicode.com/comments"
params ={
    "postId":2
}
try:
    response = requests.get(url,params=params,timeout=5)
    response.raise_for_status()
    print(response.url)
    print(response.json())
except requests.RequestException:
    print("请求失败")