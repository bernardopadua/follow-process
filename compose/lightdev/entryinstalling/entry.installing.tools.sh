#!/bin/ash

#Installing all packages resources
apk add gcc
apk add musl-dev
apk add libffi-dev
apk add openssl-dev
apk add python3
apk add python3-dev
apk add py3-pip

#Making SymLink of pyhton
ln -s /usr/bin/python3 /usr/bin/python
