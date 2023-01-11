import threading
import subprocess
from logging.handlers import RotatingFileHandler
import random
import sys
from config import rsync_bin, rsync_options, location_list


if not len(sys.argv) > 1:
    random.shuffle(location_list)

maxthreads = 3
sema = threading.Semaphore(value=maxthreads)
threads = list()


def task(value):
    sema.acquire()
    nome = value['nome']
    log_file = f'/var/log/backup{nome}.log'
    rsync_log_command = f'--log-file={log_file}'
    list_command = [
        rsync_bin,
        rsync_options,
        rsync_log_command,
        value["origin"],
        value["destin"],
    ]
    command = " ".join(list_command)
    print(command)
    rotate_log = RotatingFileHandler(log_file, backupCount=20)
    rotate_log.doRollover()
    subprocess.call(command, shell=True)
    sema.release()

if len(sys.argv) > 1:
    indice = int(sys.argv[1])
    value = location_list[indice]
    task(value)
else:
    for indice, value in enumerate(location_list):
        thread = threading.Thread(target=task, args=(value,))
        threads.append(thread)
        thread.start()
