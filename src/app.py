import os
from base64 import b64encode
from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py
import templates.deleteDB as deleteDB
from sanic import Sanic,Blueprint
from sanic.response import html,redirect
import aiofiles

app = Sanic(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.static('/static', './static')



#Open Default homepage: upload.html
@app.route("/")
async def index(request):
    #delete all data in database in homepage
    deleteDB.deleteAll()
    template = open(os.getcwd() + "/templates/upload.html")
    return html(template.read())

#Connect hompage with complete.html, and create upload and submit features


@app.route("/upload", methods=['POST'])

async def upload(request):
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)  # creat new folder if folder doesn't exist
    else:
        print("Folder already exists: {}".format(target))
    upload_file = request.files.get('file')
    if not upload_file:
        return redirect("/?error=no_file")
    file_parameters = {
        'body': upload_file.body,
        'name': upload_file.name,
        'type': upload_file.type,
    }

    file_path = "/".join([target, "temp.jpg"])
    print(file_path)
    async with open(file_path, 'wb') as f:
        f.write(file_parameters['body'])
    f.close()

    #calling test_scraper.py for image scraping after the user clicks on Submit button.
    var = test_scraper.imgurl()
    var2 = test_scraper.imgweb()
    template = open(os.getcwd() + "/templates/complete.html")
    return html(template, image_name="temp.jpg", variable=var, variable2=var2)

#Display uploaded image from user
@app.route('/upload/<filename>')
async def send_image(filename):
    return send_from_directory("images",filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)