#!/bin/bash

echo $GITHUB_REPOSITORY
URL="https://api.github.com/repos/$GITHUB_REPOSITORY/deployments"
SHA=$(cat target_sha.txt)
curl -X POST -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github.ant-man-preview+json" -H "Content-Type: application/json" $URL --data "{\"ref\": \"master\", \"required_contexts\": [], \"environment\": \"production\", \"payload\" : \"$SHA\" }"