#!/bin/ash

set -o errexit
set -o pipefail
set -o nounset

gunicorn -w 4 -b 0.0.0.0:$PORT followprocess.wsgi:application