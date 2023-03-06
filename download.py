import requests, sys

url = sys.argv[1]

file = requests.get(url)

open('download.txt', 'wb').write(file.content)

