
set -e

app="follow-process"
release="webdev"
docker_image="registry.heroku.com"

#non tty device locally
#echo "$HEROKU_PASS" | docker login -u="$HEROKU_LOGIN" --password-stdin registry.heroku.com
echo "PASSS $HEROKU_PASS"
docker login -u="$HEROKU_LOGIN" -p="$HEROKU_PASS" registry.heroku.com

docker build -t "${docker_image}/${app}/${release}" -f ./compose/lightbuild/Dockerfile.webdev .
docker push "${docker_image}/${app}/${release}"