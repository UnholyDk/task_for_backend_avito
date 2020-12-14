FROM python:3.8

RUN mkdir /app/
WORKDIR /app/
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
