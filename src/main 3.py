import os
from base64 import b64encode
# from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py
import templates.deleteDB as deleteDB
from sanic import Sanic,Blueprint
from sanic.response import html,redirect,file
from jinja2 import Template,PackageLoader,Environment
import aiofiles
import requests

app = Sanic(__name__)
env = Environment(loader=PackageLoader('main', 'templates/'))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.static('/static', './static')
app.static('/templates', './templates')
app.static('/images', './images')


#Open Default homepage: upload.html
@app.route("/")
async def index(request):
    #delete all data in database in homepage
    deleteDB.deleteAll()
    template = open(os.getcwd() + "/templates/upload.html")
    print(requests.session())
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
    with open(file_path, 'wb') as f:
        f.write(file_parameters['body'])
    f.close()

    #calling test_scraper.py for image scraping after the user clicks on Submit button.
    var = test_scraper.imgurl()
    var2 = test_scraper.imgweb()
    # word_count, entites =
    template = env.get_template('complete.html')
    content = template.render(image_name="images/temp.jpg", variable=var, variable2=var2)
    return html(content)

# image_name = tuple(*[files for (_, _, files) in os.walk('./images/')])

#Display uploaded image from user
# @app.route('/upload/<image_name>')
# async def send_image(image_name):
#     return image_name

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True,workers=4)
