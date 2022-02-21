from flask import request, render_template, redirect, url_for
from app import db
from .import bp as app
from .models import Character
from flask_login import current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')