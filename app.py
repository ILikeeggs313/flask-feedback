from flask import Flask, render_template, request, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Secret
from forms import UserForm, SecretForm
from sqlalchemy.exc import IntegrityError
#part 3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def get_register():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def registrer_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        with app.app_context():
            new_user = User.register(username, password, email,
            first_name, last_name)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('Username takent. please pick another')
                return render_template('register.html', form = form)
        session['username'] = new_user.username
        flash('welcome! Account created', 'success')
        return redirect('/secret')

@app.route('/login', methods =['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        with app.app_context():
            user = User.authenticate(username, password, email,
            first_name, last_name)
            if user:
                flash(f"Welcome back, {user.username}!", "primary")
                session['username'] = user.username
                return redirect ('/secret')
            else:
                form.username.errors = ['Invalid username/pwd']
        return render_template('login.html', form = form)

@app.route('/secret', methods = ['GET', 'POST'])
def show_secret():
    if "user_username" not in session:
        flash("please login first!", 'danger')
        return redirect('/')
    form = SecretForm()
    #we get all the secrets
    all_secrets = Secret.query.all()
    if form.validate_on_submit():
        text = form.text.data
        #we ge the user_username from the session itself
        new_secret = Secret(text = text, user_username = session['username'])
        with app.app_context():
            db.session.add(new_secret)
            db.session.commit()
            flash('new secret created!', 'success')
            return redirect('/secret')
    return render_template('secrets.html', form = form, secrets = all_secrets)


@app.route('/logout')
def logout_user():
    """log the user out"""
    with app.app_context():
        session.pop('user_username')
        flash("goodbye", "info")
        return redirect('/')

#delete a secret/feedback
@app.route('/secets/<int:id>', methods = ['POST'])
def delete_secret(id):
    """delete a secret"""
    if 'username' not in session:
        flash("Please log in first!", 'danger')
        return redirect('/')
    secret = Secret.get_or_404(id)
    if secret.user_username == session['user_username']:
        with app.app_context():
            db.session.delete(secret)
            db.session.commit()
            flash('secret deleted', 'info')
            return redirect('/secrets')
    flash("you dont have persmission to do so!", 'danger')
    return redirect('/secrets')
