# FROM python:alpine3.15
FROM python:3.9

COPY salesbot.py /salesbot/
COPY pixa_stats.py /salesbot/
COPY pymods /salesbot/
COPY ./data/db.json /salesbot/data/db.json
COPY test_data.json /salesbot/
COPY .env /salesbot/
COPY requirements.txt /tmp
RUn pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt
RUN chmod 755 /salesbot/*.py

WORKDIR /salesbot
# CMD ["python3", "--version"]
ENTRYPOINT ["python"]
CMD ["--version"]