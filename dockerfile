FROM python:3.8-slim-buster

RUN mkdir app

COPY requirements.txt /app/requirements.txt
COPY templates /app/templates
COPY app.py /app/app.py
COPY payroll.db /app/payroll.db

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]