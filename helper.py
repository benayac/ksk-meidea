import time

def sleep(sleepTime):
    for i in range(sleepTime):
        time.sleep(1)
        print(f"Sleep time left {sleepTime-i}")