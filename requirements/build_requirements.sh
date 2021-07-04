#!/bin/bash
pip-compile requirements/requirements.in

if [ "$1" == "dev" ]; then
    pip-compile requirements/requirements-dev.in
fi
