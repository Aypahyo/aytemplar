FROM python:3.11.0b3-slim-buster
WORKDIR /app
ADD . /app
ENTRYPOINT [ "python", "-m", "unittest", "discover" ]
