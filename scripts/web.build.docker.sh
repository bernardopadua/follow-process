#!/usr/bin/env bash

set -e

app="follow-process"
release="web"
docker_image="registry.heroku.com"

echo "$HEROKU_PASS" | docker login -u="$HEROKU_LOGIN" --password-stdin registry.heroku.com

docker build -t "${docker_image}/${app}/${release}" -f ./compose/lightbuild/Dockerfile.web .
docker push "${docker_image}/${app}/${release}"