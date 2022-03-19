import os
from flask import Flask, flash, redirect, render_template, url_for, request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target) #creat new folder if folder doesn't exist
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, "temp.jpg"]) #change filename inside the target folder
        print(destination)
        file.save(destination)

    return render_template("complete.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)