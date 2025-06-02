from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from app import db
from services.email_service import send_password_reset_email

password_reset_bp = Blueprint('password_reset', __name__)

@password_reset_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password form"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = user.generate_reset_token()
            send_password_reset_email(user, token)
            flash('Password reset link has been sent to your email', 'info')
        else:
            flash('Email address not found', 'error')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@password_reset_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        user.set_password(password)
        user.clear_reset_token()
        
        flash('Password has been reset successfully', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)
