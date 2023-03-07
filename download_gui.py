import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from tqdm import tqdm
import requests
import time

# Array of URLs to download
urls = [
    'http://thinkingform.com/video-sample-mp4',
    'https://file-examples.com/storage/fe0b804ac5640668798b8d0/2017/04/file_example_MP4_480_1_5MG.mp4',
    'https://file-examples.com/wp-content/uploads/2017/04/file_example_MP4_640_3MG.mp4',
]

class DownloadThread(threading.Thread):
    """
    A class that represents a download thread for a given URL.
    """

    def __init__(self, url, file_path):
        super().__init__()
        self.url = url
        self.file_path = file_path
        self.downloaded_size = 0
        self.total_size = 0
        self.downloaded_size = 0

    def run(self):
        # Download the file
        response = requests.get(self.url, stream=True)
        self.total_size = int(response.headers.get('content-length', 0))

        # Write the downloaded data to file
        with open(self.file_path, 'wb') as file:
            with tqdm(total=self.total_size, unit='B', unit_scale=True, desc=os.path.basename(self.file_path)) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    self.downloaded_size += len(data)
                    progress_bar.update(len(data))

        
    

class DownloaderApp:
    """
    A class that represents a GUI application for downloading the files.
    """

    def __init__(self, master):
        self.master = master
        master.title("File Downloader")

        # Create a label and a progress bar
        self.label = tk.Label(master, text="Downloading files...")
        self.label.pack(pady=10)
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=280, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Create a cancel button
        self.cancel_button = tk.Button(master, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=10)

        # Download the files
        self.download_files()

    def download_files(self):
        # Create a thread for each URL
        threads = []
        for url in urls:
            file_name = os.path.basename(url)
            file_path = os.path.join(os.getcwd(), file_name)
            thread = DownloadThread(url, file_path)
            threads.append(thread)

        # Start the threads
        for thread in threads:
            thread.start()

        # Update the progress bar while the threads are running
        while any(thread.is_alive() for thread in threads):
            tot_size = sum(thread.total_size for thread in threads if hasattr(thread, 'total_size'))
            downloaded_size = sum(thread.downloaded_size for thread in threads if hasattr(thread, 'downloaded_size'))
            # progress = downloaded_size / tot_size * 100 if tot_size > 0 else 0
            progress = (downloaded_size/tot_size) * 100 if tot_size > 0 else 0
            
            self.progress_bar['value'] += progress/100
            print(f"{tot_size} compare {downloaded_size}")

            self.master.update()


        # Wait for the threads to finish
        for thread in threads:
            thread.join()


        # Show a message box when the downloads are complete
        messagebox.showinfo("Download Complete", "The files have been downloaded successfully!")

    def cancel(self):
        # Terminate all the threads
        for thread in threading.enumerate():
            if isinstance(thread, DownloadThread):
                thread.terminate()

        # Close the window
        self.master.destroy()

# Create the GUI window
root = tk.Tk()
app = DownloaderApp(root)
root.mainloop()
