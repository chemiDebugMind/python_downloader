import requests
import threading
from tkinter import *
from tkinter import ttk

class Downloader:
    def __init__(self, urls):
        self.urls = urls
        self.window = Tk()
        self.window.title("File Downloader")
        self.progress = ttk.Progressbar(self.window, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(column=0, row=0, padx=10, pady=10)
        self.status = Label(self.window, text="Waiting to download...")
        self.status.grid(column=0, row=1, padx=10, pady=10)

    def downloadFile(self, url, file_name):
        self.window.after(0, self.status.configure, text=f"Downloading {file_name}...")
        file = requests.get(url, stream=True)
        if file.status_code == requests.codes.ok:
            with open(file_name, "wb") as f:
                for data in file:
                    f.write(data)
                    self.window.after(10, self.progress.step, int(100 / len(self.urls)))
                    self.window.after(10, self.status.configure, text=f"Downloading {file_name}... ({int(f.tell() * 100 / len(file.content))}%)")
        self.window.after(0, self.status.configure, text=f"{file_name} downloaded.")

    def startDownload(self):
        self.progress.configure(maximum=100)
        threads = []
        for url in self.urls:
            file_name = url.rsplit('/', 1)[1]
            t = threading.Thread(target=self.downloadFile, args=(url, file_name))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        self.window.mainloop()

if __name__ == "__main__":
    urls = [
        'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4',
        'https://download.samplelib.com/mp4/sample-5s.mp4',
        'https://download.samplelib.com/mp4/sample-10s.mp4',
    ]
    downloader = Downloader(urls)
    downloader.startDownload()
