import threading
import time


def prepare_chai(type_, wait_time):
    print(f"{type_} chai: brewing...")
    time.sleep(wait_time)
    print(f"{type_} chai: Ready.")


thread1 = threading.Thread(target=prepare_chai, args=("Masala", 2))
thread2 = threading.Thread(target=prepare_chai, args=("Ginger", 3))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

