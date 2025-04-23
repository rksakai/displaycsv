FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# 🔥 Garante que app.py será sempre atualizado
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
