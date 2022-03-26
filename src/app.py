import os
from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

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
        test_scraper.imageScrapping()

    return render_template("complete.html", image_name="temp.jpg")

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images",filename)
if __name__ == "__main__":
    app.run(port=5000, debug=True)