import json
import os.path

import requests

# update these two in order to have file run properly
file = "/home/luke/Desktop/py_filter/generated.json"
file2 = "/home/luke/Desktop/py_filter/config.yaml"
url = "http://localhost:8888/upload"


def send_request():
    files = {
        'file': open(file, 'rb'),
        'yaml': open(file2, 'rb')
        }

    r = requests.post(url, files=files)
    body = json.loads(r.content)
    with open("file_send_output.json", "w+") as out_file:
        json.dump(body, out_file, indent=6)

if __name__ == '__main__':
    send_request()
