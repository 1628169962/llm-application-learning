import time
def task(name):
    print(name + " 开始")
    time.sleep(1)
    print(name + " 完成")
start = time.perf_counter()
task("A")
task("B")
task("C")
end = time.perf_counter()
ans = end - start
print(ans)
