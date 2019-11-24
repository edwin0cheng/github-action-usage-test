#!/bin/bash

curl -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.ant-man-preview+json" -H "Content-Type: application/json" https://api.github.com/repos/$(GITHUB_REPOSITORY)/deployments --data "{\"ref\": \"master\", \"required_contexts\": [], \"environment\": \"production\", \"payload\" : \"$(cat target_sha.txt)\" }"