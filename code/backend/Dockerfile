FROM nginx:latest
#COPY nginx.conf etc/nginx/nginx.conf
COPY frontend /usr/share/nginx/html

RUN apt-get update -y && apt-get install -y python3 python3-pip
COPY mongo_http/ /code
WORKDIR /code
RUN pip3 install -r requirements.txt

CMD ["sleep", "1000"]
