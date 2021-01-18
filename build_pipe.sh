#!/usr/bin/env bash
docker build ./flaskapp -t flask_image
docker container stop flask_container
docker container rm flask_container
docker run -d --name flask_container -p 80:80 flask_image
