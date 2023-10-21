# For deployment
import os
from os.path import join, dirname
from dotenv import load_dotenv
# Flask, date,pymongo
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# GET Request handler (flask)
@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({},{"_id": False}))
    return jsonify({'articles': articles})

# POST Request handler (flask)
@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    ##### Uploading file to server
    file = request.files['file_give']
    profile = request.files['profile_give']

    # memodifikasi nama file dan memberi stamp waktu
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%d-%m-%Y %H:%M:%S')
    # mengubah save_to menjadi string dan menambahkan mytime dan modifikasi nama dari extension
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    # Untuk profile picture
    # Tidak perlu khawatir akan menimpa, karena menyimpannya dalam direktori berbeda
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    mytime = today.strftime('%d-%m-%Y %H:%M:%S')
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    # waktu ketika posting
    date = today.strftime('%d.%m.%Y')

    doc = {
        'file' : filename,
        'profile' : profilename,
        'title' : title_receive, 
        'content' : content_receive,
        'date' : date,
    }

    # inserting to selected db(which is dbsparta to collection called diary)
    db.diary.insert_one(doc)
    return jsonify({"msg": "POST request complete!"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

