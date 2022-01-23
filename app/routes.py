from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, AddressForm
from app.models import User, Address

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if either the username or email is already in db
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        # if it is, return back to register
        if user_exists:
            flash(f"User with username {username} or email {email} already exists", "danger")
            return redirect(url_for('register'))
        # Create a new user instance using form data
        User(username=username, email=email, password=password)
        flash("Thank you for registering!", "primary")
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        # Grab the data from the form
        username = form.username.data
        password = form.password.data
       
        # Query user table for user with username
        user = User.query.filter_by(username=username).first()
        
        # if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            # redirect to login page
            flash('That username and/or password is incorrect', 'danger')
            return redirect(url_for('login'))
        
        # if user does exist and correct password, log user in
        login_user(user)
        flash('You have succesfully logged in', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", "secondary")
    return redirect(url_for('index'))



@app.route('/add_address', methods=["GET","POST"])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data

        flash("Address has been added to Phone Book", "primary")
        return redirect(url_for('index'))

    return render_template('add_address.html', form=form)
