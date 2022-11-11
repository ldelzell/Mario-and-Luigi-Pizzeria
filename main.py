from flask import Blueprint, render_template
from flask import Flask, request
from flask_login import login_required
from flask_login import  current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('homepage/home.html')

@main.route('/profile')
@login_required
def profile():
    if current_user.isAdmin:
        return render_template('authentication/admin.html')
    else:
        return render_template('authentication/profile.html', name=current_user.name, email=current_user.email)
