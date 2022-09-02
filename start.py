import threading
import subprocess
import os
from pathlib import Path
from config import rsync_bin, rsync_options, location_list

maxthreads = 3
sema = threading.Semaphore(value=maxthreads)
threads = list()

def compress_file(file):
    subprocess.call(f"gzip {file}", shell=True)

def rename_file(file1, file2):
    os.rename(file1, file2)


def rotate_file(filepadrao):
    file_path = Path(filepadrao)
    file_list = file_path.parent.rglob(file_path.name + "*")
    for file_obj in file_list:
        file = str(file_obj)
        list_name_file = file.strip(".")
        if file == filepadrao:
            compress_file(file)
        elif file == filepadrao + ".gz":
            os.rename(file, file + ".1")
        elif list_name_file[3] in [str(i) for i in range(2, 20)]:
            os.rename(file, list_name_file[0] + "gz" + str(int(list_name_file[2]) + 1))
        else:
            os.remove(file)



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
    rotate_file(log_file)
    subprocess.call(command, shell=True)
    sema.release()


for indice, value in enumerate(location_list):
    thread = threading.Thread(target=task, args=(value,))
    threads.append(thread)
    thread.start()
