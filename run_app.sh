#!/usr/bin/env bash
source ~/.virtualenvs/microservices/bin/activate
python -m metric.main -l ./logging.ini -c ./config.yml