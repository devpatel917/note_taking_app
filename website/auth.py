from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db

from flask_login import login_user, login_required, logout_user, current_user

#converting password into a hash through hashing function that does not have an inverse
from werkzeug.security import generate_password_hash, check_password_hash


#applications are in encryptions for passwords
#hashng function has no inverse, given an x it will generate the same y, but with that y, we can not get the x

#if it gives the x, it can only check the hash, only check the password typed in equals the hash that is stored
auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['GET', 'POST']) #allows us to update the databse
def login():
    #if we are actually login and not just getting the page -> POST request

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        #check if email and password is valid

        #querying the database for specific user

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category = 'sucess')

                #"remembers" the fact that the user is logged in
                login_user(user, remember=True)

                #redirect user to home page if they logged in successfully

                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category = 'error')
        else:
            flash('Email does not exist', category = 'error')




    return render_template("login.html", user=current_user)

#we are not able to log out if we are not logged in
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #redirect user back to the login page
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Validation checks
        #check if user doesn't already exist
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category = 'error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 character', category = 'error')
        elif password1 != password2:
            flash('Passwords do not match', category = 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category = 'error')
        else:
            new_user = User(email=email, first_name = firstName, password =generate_password_hash(password1, method = 'sha256'))#hashing algorithm

            #add the new user to our created database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category = 'success')

            #returning the url that maps to the view associated with the function
            return redirect(url_for('views.home'))

            #add user to database

    return render_template("sign_up.html", user=current_user)
