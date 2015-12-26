
from flask import Flask, render_template,flash,session
#from content_management import Content
from dbconnect import connection  
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from pymongo import MongoClient
import gc
from flask_mail import Mail, Message

#from flask.ext.wtf import Form
#from wtforms.validators import DataRequired
#from wtforms import StringField, PasswordField,BooleanField,TextField,validators



app = Flask(__name__)




app.config.update(
        DEBUG=True,

        #EMAIL SETTINGS
        MAIL_SERVER='email-smtp.us-east-1.amazonaws.com',
        MAIL_PORT=587,
#       MAIL_USE_SSL=True,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = 'AKIAJP55YOT6BLY6S3AA',
        MAIL_PASSWORD = 'AqmlC1RF0ro/BJkakFQo5imywe5lCD0fbSBDGIH66p8G'
        #MAIL_DEFAULT_SENDER = "support@marketcalls.in"
        )
#creating mail object
mail=Mail(app)

#@app.route("/message")
def index(mailing):
        #form = RegistrationForm(request.form)
        #email=form.email.data
        msg = Message(
              'Hello',
               sender='support@marketcalls.in',
               recipients=
               [mailing])
        msg.body = "This is the email body"
        mail.send(msg)
        return "Sent"




@app.route('/')
def homepage():
    return render_template("header.html")


@app.route('/dashboard/')
def dashboard():
    flash("welcome")
    flash("to my website")
    return render_template("dashboard.html")


#user lofin functio


@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        conn = connection()
        collection=MongoClient()["blog"]["users"]
        if request.method == "POST":
            #collection = MongoClient()["blog"]["users"]

            data = collection.find_one({"username":(request.form['username'])})
            #data1=collection.find({"password":(request.form['password'])}
            #data = c.fetchone()[2]
            password=request.form['password']
            if sha256_crypt.verify(password,data['password']):
                print("password verification suceessful")
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

       # gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)  


#login required pages
'''
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap
'''
#logout

@app.route("/logout/")
#@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    #gc.collect()
    return redirect(url_for('login_page'))
		



 



#registration function
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    





@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            conn = connection()
            collection = MongoClient()["blog"]["users"]


            x =collection.find({"username":username}).count() 

            if x > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                collection.insert({"username":username,"email":email,"password":password})
                index(form.email.data)
               # conn.save()
                flash("Thanks for registering!")
               

                #c.close()
                #conn.close()
                #gc.collect()

                session['logged_in'] = True
                session['username'] = username
            
                #return(url_for('login_page'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))

 


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0',debug=True)
	  
