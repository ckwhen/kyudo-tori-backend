#!/bin/bash

echo "Export requirements"
poetry export -f requirements.txt --output requirements.txt

echo "Set Docker .env and Build"
docker-compose --env-file ./configs/.env up --build

rm ./requirements.txt
