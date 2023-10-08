from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

#create a blueprint
bp = Blueprint('auth', __name__)

# this is a hint for a login function
@bp.route('/login', methods=['GET', 'POST'])
def login(): 
    print('In Login View function')
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.query(User).filter(User.name == user_name).scalar()
        if user is None:
            error='Incorrect credentials supplied'
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error='Incorrect credentials supplied'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if next is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
            #get username, password and email from the form
            uname = register_form.user_name.data
            pwd = register_form.password.data
            email = register_form.email_id.data
            phone = register_form.phone.data
            address = register_form.address.data
            #check if a user exists
            user = db.session.query(User).filter(User.name == uname).scalar()
            if user:
                flash('Username already exists, please try another name')
                return redirect(url_for('auth.register'))
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(name=uname, password_hash=pwd_hash, email_id=email, phone_num=phone, address=address)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register_form, heading='Register')
    

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))