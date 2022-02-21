from flask_login import current_user, login_user, logout_user
from .import bp as app
from flask import render_template, redirect, url_for, request, flash
from app.blueprints.authentication.models import User
from app.blueprints.home.models import Character
from app import db
import requests
import hashlib
import random

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email.lower()).first()
        if user is None or not user.check_password(password):
            flash('Either that was an invalid password or username. Try again. ', 'danger')
            return redirect(request.referrer)
        flash('User has successfully logged in', 'success')
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('authentication/login.html')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data.get('email')).first()
        if user is not None:
            flash('That user already exists', 'warning')
            return redirect(request.referrer)
        if data.get('password') != data.get('password2'):
            flash("Your passwords don't match", 'warning')
            return redirect(request.referrer)

        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully', 'success')
        # automatically log in user on successful registration
        login_user(new_user)
        flash('User logged in successfully', 'success')
        return redirect(url_for('home.home'))

    return render_template('authentication/register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out successfully', 'primary')
    return redirect(url_for('authentication.login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        data = request.form

        user = User.query.get(current_user.id)
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')

        if (data.get('password') and data.get('password2')) and (data.get('password') == data.get('password2')):
            user.generate_password(data.get('password'))
        elif (data.get('password') or data.get('password2')):
            flash("Your passwords don't match", 'warning')
            return redirect(request.referrer)
        db.session.commit()
        flash('Your information has been updated', 'info')
        return redirect(request.referrer)
    context = {
        'character': current_user.character.all()
    }
    return render_template('authentication/profile.html', **context)

@app.route('/profile/collection', methods=['GET','POST'])
def collection():
    if request.method == 'POST':
        # Implement try except incase user searches for incorrect character or character does not exist
        try:
            hero_choice = request.form.get('character_name')
            hash = '123'+'758deeba5f42775f9fa4c0718d9a3520e137d783'+'aa16afd532773619521e9256d83b93eb'
            api_link = f'http://gateway.marvel.com/v1/public/characters?name={hero_choice}&ts=123&apikey=aa16afd532773619521e9256d83b93eb&hash={(hashlib.md5(hash.encode())).hexdigest()}'
            description_list = ['Hmmm... mysterious creature','Even Tony Stark can\'t seem to get info on them!', 'Alfred!! Sorry wrong universe', 'Lengend has it they don\'t tip well', 'Took up slam poetry in NY when Thanos killed half the universe. Saw one show... pretty good']
            power_list = ['Rocked a mask before it was COVID cool','Can perform alchemy.. water into wine anyone?', 'Super human abilities!', 'Ruthless and relentless when angry']
            s_power = random.choice(power_list)
            character_description = requests.get(api_link).json()['data']['results'][0]['description']
            if not character_description:
                character_description = random.choice(description_list)
            image_info = requests.get(api_link).json()['data']['results'][0]['thumbnail']
        except:
            flash("Either the character cannot be found or worse...you're looking for a DC character :(", 'danger')
            return redirect(request.referrer)
        
        character = Character.query.filter_by(name=hero_choice).filter_by(user_id=current_user.id).first()
        if character:
            flash("The Hero is already in your collection", 'warning')
            return redirect(url_for('authentication.collection'))
        else:
           c = Character(
                name = hero_choice,
                description = character_description,
                comics_appeared_in = requests.get(api_link).json()['data']['results'][0]['comics']['available'],
                image = image_info['path']+'.'+image_info['extension'],
                super_power = s_power,
                user_id = current_user.id,
                character_id = requests.get(api_link).json()['data']['results'][0]['id']
            )
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('authentication.collection'))

    character_context = {
        'characters': Character.query.order_by(Character.date_created.desc()).all()
    }    
    return render_template('authentication/collection.html', **character_context)

@app.route('/<id>')
def single_character(id):
    character = Character.query.get(id)
    context = {
        'character': character
    }
    return render_template('single/single.html', **context)