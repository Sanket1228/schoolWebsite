from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)

app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = params["localserver"]

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    
@app.route("/", methods=['GET','POST'])
def index():
    if(request.method=='POST'):
        name = request.form.get('Name')
        email = request.form.get('Email')
        message = request.form.get('msg')

        entry = Contacts(name=name, email = email,  message = message, date= datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template("index.html")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if(request.method=="POST"):
        username = request.form.get("uname")
        password = request.form.get("pass")
        if (username == params['admin'] and password == params['admin_pass']):
            session['user'] = username
            return render_template("dashboard.html")
    return render_template("login.html")

app.run(debug=True)
