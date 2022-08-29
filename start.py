import threading
import time
import subprocess

maxthreads = 5
sema = threading.Semaphore(value=maxthreads)
threads = list()

def task():
    sema.acquire()
    subprocess.call('find /home/daniel', shell=True)
    sema.release()

for i in range(10):
    thread = threading.Thread(target=task, args=(str(i)))
    threads.append(thread)
    thread.start()
