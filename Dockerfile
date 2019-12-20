FROM docker.io/ajay2307/aig_template:v1

USER root

COPY . /app

WORKDIR /app

RUN chmod -R 777 /app

EXPOSE 8050 8080

CMD ["python", "/app/app.py"]
 
