from threading import Lock

lock = Lock()

def update_something():
    lock.acquire()
    print("this function runs every 10 seconds")
    lock.release()


def print_hola():
    lock.acquire()
    print("HOla")
    lock.release()