from uuid import uuid4
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/logout' )
def logout():
    logout_user()
    return render_template('authentication/logout.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('authentication/login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.get(email=email)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    if user.isAdmin:
        return redirect_dest(fallback=url_for('admin'))
    else:
        return redirect_dest(fallback=url_for('main.profile'))

def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)



@auth.route('/signup')
def signup():
    return render_template('authentication/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    
    ID = uuid4()
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.get(email=email) 
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    user = User.create([ID, email, name, generate_password_hash(password)])

    return redirect(url_for('main.profile'))