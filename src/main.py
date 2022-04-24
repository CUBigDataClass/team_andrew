import os
# from flask import Flask, flash, redirect, render_template, send_from_directory, url_for, request
import templates.test_scraper as test_scraper
from templates.test_scraper import * #to import all variables from test_scraper.py

from sanic import Sanic,Blueprint
from sanic.response import html,redirect,file
from jinja2 import PackageLoader,Environment

# Users/drewbeathard/google-cloud-sdk/bin/gcloud app deploy


app = Sanic(__name__)
env = Environment(loader=PackageLoader('main', 'templates/'))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.static('/static', './static')
app.static('/templates', './templates')
app.static('/images', './images')




#Open Default homepage: upload.html
@app.route("/",methods=['POST','GET'])
async def index(request):
    if request.method == "POST":
        email = request.form.get("email")
        global username
        username = email
        template = env.get_template('upload.html')
        content = template.render(email=email)
        return html(content)
    template = open(os.getcwd() + "/templates/base.html")
    return html(template.read())
    #delete all data in database in homepage
    




#Connect hompage with complete.html, and create upload and submit features


@app.route("/upload/<username>", methods=['POST','GET'])

async def upload(request,username):
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

    file_path = "/".join([target, f"{username}.jpg"])
    with open(file_path, 'wb') as f:
        f.write(file_parameters['body'])
    f.close()

    #calling test_scraper.py for image scraping after the user clicks on Submit button.
    # var, var2, var3 = test_scraper.img(username)
    var = test_scraper.img(username)
    template = env.get_template('complete.html')
    content = template.render(image_name=f"/images/{username}.jpg", variable=var[0], variable2=var[1], variable3=var[2], variable4=var[3], variable5=var[4])# word_count=word_count, entites = entites)
    return html(content)



    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True,workers=1)