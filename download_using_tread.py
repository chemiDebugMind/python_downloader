import requests
import threading
from tqdm import tqdm


def downloadFile(url,file_name):
    file = requests.get(url, stream=True)
    total_size = int(file.headers.get('content-length', 0))
    if file.status_code == requests.codes.ok:
        with open(file_name, "wb") as f, tqdm(
            desc=file_name,
            total = total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in file:
                f.write(data)
                progress_bar.update(len(data))

    return url




urls = [
    'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4',
    'https://download.samplelib.com/mp4/sample-5s.mp4',
    'https://download.samplelib.com/mp4/sample-10s.mp4',
]


threads = []
for url in urls:
    file_name = url.rsplit('/', 1)[1]
    t = threading.Thread(target=downloadFile,args=(url,file_name))
    t.start()



