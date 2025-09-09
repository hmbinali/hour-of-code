import threading
import requests
import time


def download(url):
    print(f"Starting download from {url}")

    response = requests.get(url)
    print(f"Finished downloading from {url}, size: {len(response.content)} bytes")


urls = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg",
]


start = time.time()
threads = []

for url in urls:
    t = threading.Thread(target=download, args=(url,))
    t.start()
    threads.append(t)

for t in threads:
    t.start()

end = time.time()
print(f"All downloads done in : {end - start:.2f} seconds")
