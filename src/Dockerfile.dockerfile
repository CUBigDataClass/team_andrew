# #reset cache
# #docker-compose up
# #docker images
# #docker rmi 61717 --force
# #docker builder prune

FROM python:3.8
# FROM gcr.io/google-appengine/python	

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN apt-get install -yqq xvfb

# Set display port as an environment variable
ENV DISPLAY=:99
ENV LISTEN_PORT=5000
COPY . /main
WORKDIR /main

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4
RUN python -m spacy download en
EXPOSE 5000
# Define our command to be run when launching the container
# CMD ["gunicorn", "app:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
# CMD python3 app.py runserver 0.0.0.0:80
# CMD ["python", "./app.py", "--host", "0.0.0.0", "--port", "5000"]
CMD ["python", "./main.py"]
