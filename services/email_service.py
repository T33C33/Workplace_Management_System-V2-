from flask_mail import Message
from app import mail
from flask import current_app, url_for
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

def send_workplace_email(workplace, subject, recipients, html_body, text_body=None):
    """Send email using workplace's custom email settings"""
    if workplace.email_sender and workplace.email_password:
        try:
            # Use workplace's custom email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = workplace.email_sender
            msg['To'] = ', '.join(recipients)
            
            if text_body:
                part1 = MIMEText(text_body, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
            
            # Send via SMTP (assuming Gmail)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(workplace.email_sender, workplace.email_password)
            server.sendmail(workplace.email_sender, recipients, msg.as_string())
            server.quit()
            
        except Exception as e:
            print(f"Failed to send workplace email: {str(e)}")
            # Fallback to system email
            send_email(subject, recipients, html_body, text_body)
    else:
        # Use system email
        send_email(subject, recipients, html_body, text_body)

def send_email(subject, recipients, html_body, text_body=None):
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_body,
        body=text_body
    )
    
    # Send email asynchronously
    thread = threading.Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    )
    thread.start()

def send_password_reset_email(user, token):
    """Send password reset email"""
    subject = "Password Reset Request - Workplace Management System"
    
    reset_url = url_for('password_reset.reset_password', token=token, _external=True)
    
    html_body = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Dear {user.full_name},</p>
        
        <p>You have requested to reset your password. Click the link below to reset your password:</p>
        
        <p><a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
        
        <p>If you did not request this password reset, please ignore this email.</p>
        
        <p><strong>Note:</strong> This link will expire in 1 hour.</p>
        
        <p>Best regards,<br>
        Workplace Management Team</p>
    </body>
    </html>
    """
    
    text_body = f"""
    Password Reset Request
    
    Dear {user.full_name},
    
    You have requested to reset your password. Visit the following link to reset your password:
    
    {reset_url}
    
    If you did not request this password reset, please ignore this email.
    
    Note: This link will expire in 1 hour.
    
    Best regards,
    Workplace Management Team
    """
    
    send_email(subject, [user.email], html_body, text_body)

def send_booking_confirmation(user, booking, seat, hall, workplace, timeframe):
    subject = f"Seat Booking Confirmation - {workplace.name}"
    
    html_body = f"""
    <html>
    <body>
        <h2>Booking Confirmation</h2>
        <p>Dear {user.full_name},</p>
        
        <p>Your seat booking has been confirmed with the following details:</p>
        
        <table border="1" cellpadding="10" cellspacing="0">
            <tr><td><strong>Workplace:</strong></td><td>{workplace.name}</td></tr>
            <tr><td><strong>Hall:</strong></td><td>{hall.name}</td></tr>
            <tr><td><strong>Seat Number:</strong></td><td>{seat.seat_number}</td></tr>
            <tr><td><strong>Date:</strong></td><td>{timeframe.date}</td></tr>
            <tr><td><strong>Time:</strong></td><td>{timeframe.start_time} - {timeframe.end_time}</td></tr>
            <tr><td><strong>Booking ID:</strong></td><td>{booking.id}</td></tr>
        </table>
        
        <p><strong>Important Notes:</strong></p>
        <ul>
            <li>Please arrive on time for your booking</li>
            <li>Your booking will expire at {timeframe.end_time} on {timeframe.date}</li>
            <li>You will receive a notification when your booking expires</li>
        </ul>
        
        <p>Thank you for using our workplace management system!</p>
        
        <p>Best regards,<br>
        {workplace.name} Team</p>
    </body>
    </html>
    """
    
    text_body = f"""
    Booking Confirmation
    
    Dear {user.full_name},
    
    Your seat booking has been confirmed:
    
    Workplace: {workplace.name}
    Hall: {hall.name}
    Seat Number: {seat.seat_number}
    Date: {timeframe.date}
    Time: {timeframe.start_time} - {timeframe.end_time}
    Booking ID: {booking.id}
    
    Please arrive on time. Your booking expires at {timeframe.end_time} on {timeframe.date}.
    
    Best regards,
    {workplace.name} Team
    """
    
    # Use workplace's custom email if available
    send_workplace_email(workplace, subject, [user.email], html_body, text_body)

def send_expiry_notification(user, booking, seat, hall, workplace, timeframe):
    subject = f"Seat Booking Expired - {workplace.name}"
    
    html_body = f"""
    <html>
    <body>
        <h2>Booking Expiry Notification</h2>
        <p>Dear {user.full_name},</p>
        
        <p>Your seat booking has expired:</p>
        
        <table border="1" cellpadding="10" cellspacing="0">
            <tr><td><strong>Workplace:</strong></td><td>{workplace.name}</td></tr>
            <tr><td><strong>Hall:</strong></td><td>{hall.name}</td></tr>
            <tr><td><strong>Seat Number:</strong></td><td>{seat.seat_number}</td></tr>
            <tr><td><strong>Date:</strong></td><td>{timeframe.date}</td></tr>
            <tr><td><strong>Time:</strong></td><td>{timeframe.start_time} - {timeframe.end_time}</td></tr>
            <tr><td><strong>Booking ID:</strong></td><td>{booking.id}</td></tr>
        </table>
        
        <p>The seat is now available for other bookings.</p>
        
        <p>Thank you for using our workplace management system!</p>
        
        <p>Best regards,<br>
        {workplace.name} Team</p>
    </body>
    </html>
    """
    
    # Use workplace's custom email if available
    send_workplace_email(workplace, subject, [user.email], html_body)

def send_admin_notification(admin_email, subject, message):
    """Send notification to admin"""
    html_body = f"""
    <html>
    <body>
        <h2>Admin Notification</h2>
        <p>{message}</p>
        
        <p>Best regards,<br>
        Workplace Management System</p>
    </body>
    </html>
    """
    
    send_email(subject, [admin_email], html_body)
