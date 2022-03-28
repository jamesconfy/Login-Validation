from flask import request, render_template, redirect, url_for, flash
from flask import current_app
from login_validation import db, bcrypt
from flask_login import login_required, logout_user, current_user, login_user
from login_validation.forms import RegistratrionForm, LoginForm, UpdateAccountForm
from login_validation.models import User

app = current_app

@app.route('/')
@app.route('/home')
def home():
    data = User.query.all()
    return render_template('home.html', title='Home', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistratrionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            # city = request.form['city']
            user = User(username=form.username.data, password=hashed_password, email=form.email.data, first_name=form.first_name.data,
                        last_name=form.last_name.data, dob=form.dob.data, address=form.address.data, city=form.city.data, state=form.state.data, phone_no=form.phone_no.data)
            db.session.add(user)
            db.session.commit()
            flash('Account Created Successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)

                next_url = request.form.get('next')
                if next_url:
                    return redirect(next_url)
            else:
                flash('Login Unsucessful, check username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.dob = form.dob.data
            current_user.address = form.address.data
            current_user.city = form.city.data
            current_user.state = form.state.data
            current_user.phone_no = form.phone_no.data
            db.session.commit()
            flash('Account Updated Successfully', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.dob.data = current_user.dob
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.phone_no.data = current_user.phone_no
    return render_template('account.html', title='Account', form=form)


@app.route('/delete_profile')
@login_required
def delete_profile():
    db.session.delete(current_user)
    db.session.commit()
    flash(f'User Deleted Successfully')
    return redirect(url_for('home_page'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logout successfully')
    return redirect(url_for('home'))