# FROM python:alpine3.15
FROM python:3.9

COPY salesbot.py /salesbot/
# Note, if you run docker with docker run -v ~/salesbot/data:/salesbot/data ,
# only the local host file on the VM (~/salesbot/data) is used .. it's the host's
# data dir that gets mounted , not the containers, so even though this Dockerfile
# has the below COPY statement for db.json, it's really only useful for testing locally
# and running docker without a -v <hostdir>:<containerdir> flag.
COPY ./data/db.json /salesbot/data/db.json
COPY .env /salesbot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
RUN chmod 755 /salesbot/*.py

WORKDIR /salesbot
# CMD ["python3", "--version"]
ENTRYPOINT ["python"]
CMD ["--version"]