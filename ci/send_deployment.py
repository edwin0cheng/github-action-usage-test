import sys
import os
import json
import subprocess

print(os.environ['GITHUB_REPOSITORY'])

url = "https://api.github.com/repos/{}/deployments".format(os.environ['GITHUB_REPOSITORY'])
sha = open("target_sha.txt", "r").read().strip()
issue = json.load(open("issue.json", "r"))
payload = dict()
payload["sha"] = sha
payload["issue"] = issue

payload_str = json.dumps(payload)

data = dict()
data["ref"] = "master"
data["required_contexts"] = []
data["environment"] = "production"
data["payload"] = payload_str

subprocess.run([
    "curl", 
    "-X", 
    "POST", 
    "-H", "Authorization: token " + os.environ["TOKEN"],
    "-H", "Accept: application/vnd.github.ant-man-preview+json", 
    "-H", "Content-Type: application/json",
    url,
    "--data", json.dumps(data)
    ])


# echo $GITHUB_REPOSITORY
# URL="https://api.github.com/repos/$GITHUB_REPOSITORY/deployments"
# SHA=$(cat target_sha.txt)
# printf -v ISSUE "%q" "$(cat issue.json)"

# # We need quote the double quote as it is used in a quote later
# PAYLOAD="{ \\\"sha\\\" : \\\"$SHA\\\", \\\"issue\\\" : $ISSUE }"

# echo curl -X POST -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github.ant-man-preview+json" -H "Content-Type: application/json" $URL --data "{\"ref\": \"master\", \"required_contexts\": [], \"environment\": \"production\", \"payload\" : \"$PAYLOAD\" }"    