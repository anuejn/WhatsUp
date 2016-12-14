FROM debian:latest
RUN apt-get -y update && apt-get install -y python3 python3-pip
COPY . root/
RUN pip3 install -r root/requirements.txt

CMD ["python3", "root/src/zeit.py"]
