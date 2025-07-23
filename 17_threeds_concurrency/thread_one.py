import threading
import time


def boil_milk():
    print("Boiling milk...")
    time.sleep(2)
    print("milk boiled...")


def toast_bun():
    print("Toasting bun...")
    time.sleep(2)
    print("Bun toasted...")


start = time.time()

thread1 = threading.Thread(target=boil_milk)
thread2 = threading.Thread(target=toast_bun)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

end = time.time()

print(f"Breakfast is ready in : {end - start:.2f} seconds")
