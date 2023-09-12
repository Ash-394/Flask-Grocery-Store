from xmlrpc.client import boolean
from flask import Blueprint,render_template, request,flash, redirect, url_for,session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)
ADMIN_AUTH_KEY = 'ASDFGH123'

# Helper function to check if the user is logged in as admin
def is_admin():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return user.role == 'admin'
    return False

# Route for admin/user login
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # 'admin' or 'user'

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                session['user_id'] = user.id
                if role == 'admin':
                    
                    return redirect(url_for('routes.admin_dashboard'))
                else:
                    return redirect(url_for('routes.user_dashboard'))

        flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html',user=current_user)

#Route for admin/user logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Route for admin/user signup
@auth.route('/signup', methods=['GET','POST'])
def SignUp():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        authkey = request.form.get('authkey')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif not username or not role or not password1 or not password2 or role == "":
            flash('Please fill out all the fields.', 'error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif authkey != ADMIN_AUTH_KEY:
                flash('Admin authentication failed!', category='error')

        else:
            new_user = User(username=username,password=generate_password_hash(password1, method='sha256'),role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user,remember=True)
            if role == 'admin':
                return redirect(url_for('routes.admin_dashboard'))
            else:
                return redirect(url_for('routes.user_dashboard'))
    return render_template('signup.html',user=current_user)