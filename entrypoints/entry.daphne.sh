#!/bin/bash
cd follow-process && exec daphne -b 0.0.0.0 -p 8001 followprocess.asgi:application