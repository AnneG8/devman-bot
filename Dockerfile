FROM python:3.10-slim

COPY requirements.txt /opt/devman-bot/requirements.txt

WORKDIR /opt/devman-bot

RUN pip install -r requirements.txt

COPY . /opt/devman-bot

CMD ["python3.10", "main.py"]
