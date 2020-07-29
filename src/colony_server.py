from flask import Flask, request, flash, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'images'
COLONIES_FILENAME="colonies.jpg"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


commands=[]

@app.route("/")
@cross_origin() # allow all origins all methods.
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/get")
@cross_origin() # allow all origins all methods.
def getCommand():
  cmd=""
  params=""
  if commands:
    line=commands.pop()
    args=line.split(None, 1)
    cmd=args[0]
    if len(args)>1:
        params=args[1]

    print(cmd,params)
    
  return jsonify({'cmd':cmd,'params':params})
  
@app.route("/addCommand",methods = ['GET', 'POST'])
def addCommand():
	
	content=request.json
	cmd=json.loads(content)
	
	commands.append(cmd['cmd'])
	
	return "OK"


@app.route("/uploadPicture",methods = ['GET', 'POST'])
def upload_file():

    from werkzeug.datastructures import FileStorage
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], COLONIES_FILENAME))
    return 'OK', 200


@app.route("/getImageFilename")
@cross_origin() # allow all origins all methods.
def getImagefilename():
  
  return UPLOAD_FOLDER+"/"+COLONIES_FILENAME

app.run("0.0.0.0")
