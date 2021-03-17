from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)

app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = params["localserver"]

db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_pass']
)
mail = Mail(app)

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
        mail.send_message('New Message from ' + name,
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message
                          )

    return render_template("index.html",params=params)

app.run(debug=True)
