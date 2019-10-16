FROM docker.io/ajay2307/aig_template:v1

COPY . /app

WORKDIR /app

EXPOSE 8050 8080

CMD ["python", "/app/app.py"]
 
