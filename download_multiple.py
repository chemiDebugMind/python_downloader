import requests
from multiprocessing.pool import ThreadPool
import progressbar 


def downloadUrl(url):

    file_name = url.rsplit('/', 1)[-1]
    print(file_name)
    file = requests.get(url,stream=True)
    if file.status_code == requests.codes.ok:
        with open(file_name, 'wb') as f:
            for data in file:
                f.write(data)
                
    return url

urls = [
    'https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4',
    'https://download.samplelib.com/mp4/sample-5s.mp4',
    'https://download.samplelib.com/mp4/sample-10s.mp4',
]


results = ThreadPool(3).imap_unordered(downloadUrl, urls)

widgets = ['Loading: ', progressbar.AnimatedMarker()]
bar = progressbar.ProgressBar(widgets=widgets).start()

for r in results:
    print(r)
    
