#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/follow-process