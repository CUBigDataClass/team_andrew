import os
from base64 import b64encode
from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py
import templates.deleteDB as deleteDB

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Open Default homepage: upload.html
@app.route("/")
def index():
    #delete all data in database in homepage
    deleteDB.deleteAll()
    return render_template("upload.html")

#Connect hompage with complete.html, and create upload and submit features
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
        os.mkdir(target) #creat new folder if folder doesn't exist
    else:
        print("Folder already exists: {}".format(target))

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, "temp.jpg"]) #change filename inside the target folder
        file.save(destination)

    #calling test_scraper.py for image scraping after the user clicks on Submit button.
    var = test_scraper.imageScrapping()

    return render_template("complete.html", image_name="temp.jpg", variable=var)

#Display uploaded image from user
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images",filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)