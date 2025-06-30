FROM python:3.11

WORKDIR /my_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["fastapi", "dev", "app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
