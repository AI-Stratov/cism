#!/bin/bash

dockerize -wait tcp://db:5432 -timeout 60s

dockerize -wait tcp://kafka:9092 -timeout 60s

uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info
