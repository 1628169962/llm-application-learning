import time
def request(name):
    print(name+"开始")
    time.sleep(2)
    print(name + "结束")
start = time.perf_counter()
request("request-1")
request("request-2")
request("request-3")
end = time.perf_counter()
ans = end - start
print(ans)