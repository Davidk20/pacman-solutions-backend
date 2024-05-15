FROM python:3.10-alpine
WORKDIR /backend
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 8080
WORKDIR /backend/
CMD exec gunicorn --workers 1 --bind :8080 wsgi:app
