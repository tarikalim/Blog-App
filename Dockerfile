FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=Backend_Frontend/app.py
ENV FLASK_ENV=development

EXPOSE 5000

RUN python Backend_Frontend/init_db.py

CMD ["flask", "run", "--host=0.0.0.0"]
