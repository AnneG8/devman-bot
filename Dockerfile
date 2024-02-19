FROM python:3.10-slim

WORKDIR /opt/devman-bot

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install -r /tmp/requirements.txt

COPY . /opt/devman-bot

CMD ["python3.10", "main.py"]
