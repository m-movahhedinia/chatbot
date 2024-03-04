FROM python:3.11
LABEL authors="mansour"

WORKDIR /vector_store

COPY . .

RUN pip install -r requirements.txt

EXPOSE 2024

CMD python -m service.serve
