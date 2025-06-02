from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from models import Workplace, Hall, Seat
from app import db
import os
from werkzeug.utils import secure_filename

workplace_bp = Blueprint('workplace', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@workplace_bp.route('/<int:workplace_id>')
@login_required
def workplace_profile(workplace_id):
    workplace = Workplace.query.get_or_404(workplace_id)
    halls = Hall.query.filter_by(workplace_id=workplace_id, is_active=True).all()
    
    # Get total seats count
    total_seats = 0
    for hall in halls:
        total_seats += len(hall.seats)
    
    return render_template('workplace/profile.html', 
                         workplace=workplace, 
                         halls=halls,
                         total_seats=total_seats)

@workplace_bp.route('/<int:workplace_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workplace_profile(workplace_id):
    workplace = Workplace.query.get_or_404(workplace_id)
    
    # Check if user is admin
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('workplace.workplace_profile', workplace_id=workplace_id))
    
    if request.method == 'POST':
        workplace.about = request.form.get('about', '')
        workplace.website = request.form.get('website', '')
        workplace.phone = request.form.get('phone', '')
        workplace.contact_email = request.form.get('contact_email', '')
        workplace.operating_hours = request.form.get('operating_hours', '')
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                import time
                filename = f"{int(time.time())}_{filename}"
                
                logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'workplace_logos', filename)
                file.save(logo_path)
                workplace.logo_filename = filename
        
        db.session.commit()
        flash('Workplace profile updated successfully!', 'success')
        return redirect(url_for('workplace.workplace_profile', workplace_id=workplace_id))
    
    return render_template('workplace/edit_profile.html', workplace=workplace)

@workplace_bp.route('/<int:workplace_id>/halls/<int:hall_id>/seats')
@login_required
def hall_seat_arrangement(workplace_id, hall_id):
    workplace = Workplace.query.get_or_404(workplace_id)
    hall = Hall.query.filter_by(id=hall_id, workplace_id=workplace_id).first_or_404()
    seats = Seat.query.filter_by(hall_id=hall_id, is_active=True).all()
    
    return render_template('workplace/seat_arrangement.html', 
                         workplace=workplace, 
                         hall=hall, 
                         seats=seats)

@workplace_bp.route('/api/seats/<int:seat_id>/position', methods=['POST'])
@login_required
def update_seat_position(seat_id):
    if not current_user.is_admin:
        return {'error': 'Admin access required'}, 403
    
    seat = Seat.query.get_or_404(seat_id)
    data = request.get_json()
    
    seat.position_x = data.get('x', 0)
    seat.position_y = data.get('y', 0)
    
    db.session.commit()
    
    return {'success': True}
