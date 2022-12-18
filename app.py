from flask import Flask,request
import os, gridfs, pika, json
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storageAPI  import utililty

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(app)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.route("/login", methods=['POST'])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file per request", 400

        for _, f in request.files.items():
            err = utility.upload(f, fs, channel, access)

            if err:
                return err

        return "success!", 200

    else:
        return "Unauthorised", 403




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
