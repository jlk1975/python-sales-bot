# FROM python:alpine3.15
FROM python:3.9

COPY salesbot.py /bot/
COPY stats.py /bot/
COPY pymods /bot/pymods
COPY ./data/db.json /bot/data/db.json
COPY test_data.json /bot/
COPY .env /bot/
COPY requirements.txt /bot/
RUn pip3 install --upgrade pip
RUN pip3 install -r /bot/requirements.txt
RUN chmod 755 /bot/*.py

WORKDIR /bot
ENTRYPOINT ["python"]
CMD ["--version"]