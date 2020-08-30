#!/bin/ash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

celery worker -A followprocess -l info