import time
def task(name):
    print(name + " 开始请求")
    time.sleep(2)
    print(name +" 请求完成")

start = time.perf_counter()
task("A")
task("B")
task("C")
end = time.perf_counter()
ans = end - start
print(ans)