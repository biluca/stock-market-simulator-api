FROM python

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY . .

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

RUN make migrations

RUN make migrate

CMD ["make", "run"]