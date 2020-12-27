from flask import Flask, request, render_template, redirect, url_for, session, flash, request
from flask_bcrypt import Bcrypt
from db import *
from forms import RegistratrionForm, LoginForm, UpdateAccountForm
from datetime import timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)

# must be set to use sessions
app.config['SECRET_KEY'] = '6878efc95d36a4e61b9698c6e8122fee'
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        db = DB()

        data = db.GetByID(user_id[0])
        return render_template('home.html', title='Home', data=data)
    else:
        return render_template('home.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = DB()

    form = RegistratrionForm(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        state = request.form['state']
        db.CreateProfile(form.username.data, hashed_password, form.email.data, form.first_name.data, form.last_name.data, form.dob.data, form.address.data, form.city.data, state, form.phone_no.data)
        flash('Account Created Successfully', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = DB()

    form = LoginForm()
    if form.validate_on_submit():
        user = db.GetByUsername(form.username.data)
        
        if user != None:
            if bcrypt.check_password_hash(user[2], form.password.data.encode('utf-8')):
                user_id = db.GetIDBy_Username_Password(form.username.data)
                session['user_id'] = user_id

                data = db.GetByID(user_id[0])
                next_page = request.args.get('next')
                flash('Logged In Successfully', 'success')
                return redirect(next_page) if next_page else render_template('home.html', title='Dashboard', data=data)
        else:
            flash('Username or Password Incorrect', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


# @app.route('/signin', methods=['POST', 'GET'])
# def signin():
#     if request.method == 'POST':
#         db = DB()

#         username = request.form['username']
#         password = request.form['password']

#         hashed_pass = db.GetPasswordByUsername(username)
#         if hashed_pass != None:
#             if bcrypt.generate_password_hash(hashed_pass[0], password) == True:
#                 user_id = db.GetIDBy_Username_Password(username)
#                 session['user_id'] = user_id

#                 data = db.GetByID(user_id[0])
#                 return render_template('viewprofile.html', title='Dashboard', data=data)

#         else:
#             flash("Username or Password Incorrect", "info")
#             return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
def account():
    id = request.args['id']
    db = DB()
    get_user = db.GetByID(id)

    form = UpdateAccountForm()
    if form.validate_on_submit():
        db.UpdateAll(id, form.username.data, form.email.data, form.first_name.data,
             form.last_name.data, form.dob.data, form.address.data, form.city.data, form.state.data, form.phone_no.data)
        flash('Account Updated Successfully', 'success')
        return redirect(url_for('account', id=id))

    elif request.method == 'GET':
        form.username.data = get_user[1]
        form.email.data = get_user[3]
        form.first_name.data = get_user[4]
        form.last_name.data = get_user[5]
        form.dob.data = get_user[6]
        form.address.data = get_user[7]
        form.city.data = get_user[8]
        form.state.data = get_user[9]
        form.phone_no.data = get_user[10]

    return render_template('account.html', title='Account', data=get_user, form=form)


@app.route('/delete_profile')
def delete_profile():
    db = DB()
    id = request.args["id"]

    db.DeleteProfileByID(id)
    return redirect(url_for('home_page'))
    

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)

        flash('You have logout successfully')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
