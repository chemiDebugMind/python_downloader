import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from tqdm import tqdm
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl

# Array of URLs to download
urls = [
    'http://thinkingform.com/video-sample-mp4',
    'https://jsoncompare.org/LearningContainer/SampleFiles/Video/MP4/sample-mp4-file.mp4',
    'https://filesamples.com/formats/mp4/samples/video/mp4/sample_960x540.mp4',
]

class DownloadThread(threading.Thread):
    """
    A class that represents a download thread for a given URL.
    """

    def __init__(self, url, file_path):
        super().__init__()
        self.url = url
        self.file_path = file_path
        self.total_size = 0
        self.downloaded_size = 0
        # self.receiver_email = receiver_email
        

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
    A class that represents a GUI application for downloading the files. Send an email with file attachment
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

         # Create entry fields for receiver email
        self.receiver_email_label = tk.Label(master, text="To Email:")
        self.receiver_email_label.pack(pady=5)
        self.receiver_email_entry = tk.Entry(master)
        self.receiver_email_entry.pack(pady=5)
        self.send_email_button = tk.Button(master, text="Send Email", command=self.send_email)
        self.send_email_button.pack(pady=10)
        
        self.all_files = []

        # Download the files
        self.download_files()

    def download_files(self):
        # Create a thread for each URL
        threads = []
        for url in urls:
            file_name = os.path.basename(url)
            file_path = os.path.join(os.getcwd(), file_name)
            thread = DownloadThread(url, file_path)
            self.all_files.append(file_path)
            threads.append(thread)


        # Start the threads
        for thread in threads:
            thread.start()

        # Update the progress bar while the threads are running
        while any(thread.is_alive() for thread in threads):
            tot_size = sum(thread.total_size for thread in threads if hasattr(thread, 'total_size'))
            downloaded_size = sum(thread.downloaded_size for thread in threads if hasattr(thread, 'downloaded_size'))
            progress = (downloaded_size/tot_size)*100  if tot_size > 0 else 0
            self.progress_bar['value'] = progress
            # print(f"{tot_size}  - {downloaded_size}")
            # print(self.progress_bar["value"])
            self.master.update()


        # Wait for the threads to finish
        for thread in threads:
            thread.join()

        # Show a message box when the downloads are complete
        messagebox.showinfo("Download Complete", "The files have been downloaded successfully!")

    def send_email(self):
        # Get the receiver email address from the entry field
        receiver_email = self.receiver_email_entry.get()

        # Create a thread to send the email
        thread = threading.Thread(target=self._send_email, args=(receiver_email,))
        thread.start()

    def _send_email(self,receiver_email):
        # Create the message object
        message = MIMEMultipart()
        message['Subject'] = 'Downloaded File'
        message['From'] = 'tenzinchemi50@gmail.com'
        message['To'] = receiver_email

        # Attach the downloaded file to the message
        for files in self.all_files:
            with open(files, 'rb') as file:
                
                attachment = MIMEApplication(file.read(), _subtype='mp4')
                attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(files))
                message.attach(attachment)

        # Send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login('tenzinchemi50@gmail.com', 'xolefunnoxgdisfb')
            smtp.sendmail('tenzinchemi50@gmail.com', receiver_email, message.as_string())
        print('Email sent successfully.')
    

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
