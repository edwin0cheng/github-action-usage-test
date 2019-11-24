#!/bin/bash

echo $GITHUB_REPOSITORY
URL="https://api.github.com/repos/$GITHUB_REPOSITORY/deployments"

curl -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.ant-man-preview+json" -H "Content-Type: application/json" $URL --data "{\"ref\": \"master\", \"required_contexts\": [], \"environment\": \"production\", \"payload\" : \"${cat target_sha.txt}\" }"