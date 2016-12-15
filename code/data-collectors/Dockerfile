FROM python:3

COPY requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt

COPY . /code

CMD ["python", "zeit.py"]
