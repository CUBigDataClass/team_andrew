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
app.config.REQUEST_TIMEOUT = 30




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

    new_var = []
    new_url = []
    new_web = []
    print(var[0], len(var[0]))
    print()
    print(var[1], len(var[1]))
    print()
    print(var[2], len(var[2]))
    data = var[2]
    print("000:", var[0])
    
    while data:
        minimum = min(data)
        print("min: ", minimum)
        position = data.index(minimum)
        print("pos: ", position)
        new_url.append(var[0][position])
        print(new_url)
        new_web.append(var[1][position])
        print(new_web)
        new_var.append(minimum)
        data.remove(minimum)
    
    new_var.reverse()
    new_url.reverse()
    new_web.reverse()
    

    content = template.render(image_name=f"/images/{username}.jpg", variable=new_url, variable2=new_web, variable3=new_var, variable4=var[3], variable5=var[4])# word_count=word_count, entites = entites)
    return html(content)



    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True,workers=1)