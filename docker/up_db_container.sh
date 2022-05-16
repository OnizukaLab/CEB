#!/bin/bash

export LCARD_USER=ceb
export LCARD_PORT=5432
docker build --build-arg LCARD_USER=${LCARD_USER} -t pg12 .
docker run --rm -d --shm-size=1g --network ceb --name card-db -p ${LCARD_PORT}:5432 -d pg12
docker restart card-db
docker exec card-db /imdb_setup.sh
