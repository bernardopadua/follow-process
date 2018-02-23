#!/usr/bin/env bash

cd follow-process && celery worker -A followprocess -l info