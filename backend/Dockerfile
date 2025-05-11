FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["python3", "manage.py", "migrate"] 

# CMD ["python3", "manage.py", "runserver", "0:8000"]
CMD ["/app/container-entry-point.sh"]
