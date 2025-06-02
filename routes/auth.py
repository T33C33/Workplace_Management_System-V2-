from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from app import db
import re
from models.workplace import Workplace

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        workplace_id = request.form.get('workplace_id')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            # For non-admin users, associate with selected workplace
            if not user.is_admin and workplace_id:
                user.workplace_id = workplace_id
                db.session.commit()
            
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    # Get all active workplaces for selection
    workplaces = Workplace.query.filter_by(is_active=True).all()
    return render_template('auth/login.html', workplaces=workplaces)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        workplace_id = request.form.get('workplace_id')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html', workplaces=Workplace.query.filter_by(is_active=True).all())
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html', workplaces=Workplace.query.filter_by(is_active=True).all())
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('auth/register.html', workplaces=Workplace.query.filter_by(is_active=True).all())
        
        if not User.validate_phone_number(phone_number):
            flash('Invalid Nigerian phone number format', 'error')
            return render_template('auth/register.html', workplaces=Workplace.query.filter_by(is_active=True).all())
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            workplace_id=workplace_id
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    workplaces = Workplace.query.filter_by(is_active=True).all()
    return render_template('auth/register.html', workplaces=workplaces)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
