
from flask import Flask, render_template, request,url_for,Response,make_response
from werkzeug import parse_options_header
from google.cloud import storage




import datetime
import hashlib 
import json
import os

default_bucket="%s.appspot.com" %os.environ['GOOGLE_CLOUD_PROJECT']
client = storage.Client().from_service_account_json("service.json")
bucket = storage.Bucket(client, default_bucket)

app = Flask(__name__)


@app.route('/form')
def form():
    return render_template('index.html')

@app.route('/get_signed_url', methods=['GET'])
def get_signed_url():
    filename = request.args.get('filename')
    content_type =request.args.get('content_type')
    file_blob = bucket.blob(filename, chunk_size=262144 * 5)
    url = file_blob.generate_signed_url(datetime.datetime.now() + datetime.timedelta(hours=2), method='PUT',content_type=content_type)
    
    data = {'url': url, 'key': hashlib.md5(filename.encode('utf-8')).hexdigest()}
    response=make_response(json.dumps(data));
    return response

@app.route('/upload_callback', methods=['POST'])
def upload_callback():
    filename = request.form['file_name']
    file_blob = bucket.blob(filename, chunk_size=262144 * 5)
    url = file_blob.generate_signed_url(datetime.datetime.now() + datetime.timedelta(hours=2), method='GET')
    return render_template('uploaded_file.html',url =url) 

@app.route('/liveness_check', methods=['GET'])
def liveness_check():

    return make_response("ok") 


