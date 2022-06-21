FROM python:latest
WORKDIR /app
RUN python -m pip install --upgrade pip
ADD . /app
ENTRYPOINT [ "python", "-m", "unittest", "discover" ]
