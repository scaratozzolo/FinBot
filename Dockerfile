FROM python:3.11

RUN pip install GroupyAPI
RUN pip install -r requirements.txt

CMD gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080