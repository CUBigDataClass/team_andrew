# #reset cache
# #docker-compose up
# #docker images
# #docker rmi 61717 --force
# #docker builder prune

FROM python:3.8


# Set display port as an environment variable
ENV DISPLAY=:99
ENV LISTEN_PORT=3000
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
EXPOSE 3000

# Define our command to be run when launching the container
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
# CMD python3 app.py runserver 0.0.0.0:80
# CMD ["python", "./app.py", "--host", "0.0.0.0", "--port", "5000"]
# CMD ["python", "./app2.py"]
CMD ["python", "./app2.py", "--host", "0.0.0.0", "--port", "3000"]