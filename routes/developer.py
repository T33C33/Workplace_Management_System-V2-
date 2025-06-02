from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models.developer import Developer
from app import db
import os
from werkzeug.utils import secure_filename
import json

developer_bp = Blueprint('developer', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@developer_bp.route('/info')
@login_required
def developer_info():
    # Get or create developer info
    developer = Developer.query.first()
    if not developer:
        # Create default developer info
        developer = Developer(
            name="Teecee Iheukwumere",
            email="teeceeiheukwumere@gmail.com",
            bio="Full-stack developer passionate about creating efficient workplace management solutions.",
            skills=json.dumps([
                "Python", "Flask", "JavaScript", "HTML/CSS", "MySQL", 
                "Bootstrap", "Git", "Docker", "Linux", "API Development"
            ]),
            github_url="https://github.com/teecee",
            linkedin_url="https://linkedin.com/in/teecee",
            portfolio_url="https://teecee-portfolio.com"
        )
        db.session.add(developer)
        db.session.commit()
    
    # Parse skills JSON
    try:
        skills = json.loads(developer.skills) if developer.skills else []
    except:
        skills = []
    
    return render_template('developer/info.html', developer=developer, skills=skills)

@developer_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_developer_info():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('developer.developer_info'))
    
    developer = Developer.query.first()
    if not developer:
        developer = Developer()
        db.session.add(developer)
    
    if request.method == 'POST':
        developer.name = request.form.get('name', '')
        developer.email = request.form.get('email', '')
        developer.bio = request.form.get('bio', '')
        developer.github_url = request.form.get('github_url', '')
        developer.linkedin_url = request.form.get('linkedin_url', '')
        developer.portfolio_url = request.form.get('portfolio_url', '')
        
        # Handle skills
        skills_input = request.form.get('skills', '')
        skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        developer.skills = json.dumps(skills_list)
        
        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                import time
                filename = f"developer_{int(time.time())}_{filename}"
                
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'developer', filename)
                file.save(image_path)
                developer.profile_image = filename
        
        db.session.commit()
        flash('Developer information updated successfully!', 'success')
        return redirect(url_for('developer.developer_info'))
    
    # Parse skills for editing
    try:
        skills = json.loads(developer.skills) if developer.skills else []
        skills_string = ', '.join(skills)
    except:
        skills_string = ''
    
    return render_template('developer/edit_info.html', developer=developer, skills_string=skills_string)
