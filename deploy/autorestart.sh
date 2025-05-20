#!/bin/bash
while true; do
  docker-compose down
  docker-compose up --build -d
  sleep 60
done