import time
def countdown(n):
    for i in range(n, 0, -1):
        yield i

def bar_loop():
    for i in range(0, 101, 10):
        print(f"Progress: {i:3d}%", end="\r")
        time.sleep(0.1)
    print()
bar_loop()