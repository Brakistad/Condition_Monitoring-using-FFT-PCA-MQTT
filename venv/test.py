import threading
import time
def meth(n):
    i=0
    while i<n:
        i = i + 1
        time.sleep(1)
        print(i)
    return n
a = 10
t = threading.Thread(target=meth, args=(a,))
t.start()

while(t.is_alive()):
    time.sleep(1)
    print("thread is still alive")
print("thread is dead")
