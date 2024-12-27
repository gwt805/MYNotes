FROM python:3.11-bookworm

RUN mkdir -p /app/Server

WORKDIR /app/Server

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "db/dbopt.py", "--type", "create"]