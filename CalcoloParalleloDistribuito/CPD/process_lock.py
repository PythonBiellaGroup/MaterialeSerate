import multiprocessing
import sys


# FONTE: https://pymotw.com/2/multiprocessing/communication.html

def worker_with(lock, stream):
    """Acquisizione lock con statement with"""
    with lock:
        stream.write('Lock acquired via with\n')


def worker_no_with(lock, stream):
    """Acquisizione lock diretta"""
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()


lock = multiprocessing.Lock()
w = multiprocessing.Process(target=worker_with, args=(lock, sys.stdout))
nw = multiprocessing.Process(target=worker_no_with, args=(lock, sys.stdout))

w.start()
nw.start()

w.join()
nw.join()