import threading
import subprocess
from config import rsync_bin, rsync_options, location_list

maxthreads = 3
sema = threading.Semaphore(value=maxthreads)
threads = list()

def task(i):
    sema.acquire()
    list_command = ['echo', rsync_bin, rsync_options, location_list[i]['origin'], location_list[i]['destini']]
    command = ' '.join(list_command)
    print(command)
    subprocess.call(command, shell=True)
    sema.release()

for indice, value in enumerate(location_list):
    print(indice)
    thread = threading.Thread(target=task, args=(str(indice)))
    threads.append(thread)
    thread.start()
