from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')




from app import app  
from flask import request, redirect, render_template, url_for, flash  
from flask.ext.login import login_user, logout_user  
from .forms import LoginForm  
from .user import User

@app.route('/signUp', methods=['GET', 'POST'])
def login():  
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash(" signuped successfully", category='success')
            return redirect(request.args.get("next") or url_for("writePost"))
        flash("Wrong username or password", category='error')
    return render_template('signup.html', title='signup', form=form)





if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
