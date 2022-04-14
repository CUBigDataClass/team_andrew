# -*- coding: utf-8 -*-

from app import app

if __name__ == '__main__':
    # Running app in debug mode
    app.run(debug=True)

# run the following in terminal:
# mongosh "mongodb+srv://cluster1.jsqyd.mongodb.net/ImageSearch" --apiVersion 1 --username team_andrew
# enter the password when prompted --> this will start up the mongo server

#in separate terminal run:
# mongod

# in separate terminal run run-app.py
#do any GET/POST/DELETE calls


# https://www.youtube.com/watch?v=nwgQzuRRgec
# https://www.moesif.com/blog/technical/restful/Guide-to-Creating-RESTful-APIs-using-Python-Flask-and-MongoDB/