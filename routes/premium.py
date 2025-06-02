from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import *
from app import db
from services.payment_service import PaymentService, check_master_access
from services.ai_chatbot import AIChatbot
from datetime import datetime, timedelta
import json

premium_bp = Blueprint('premium', __name__)

@premium_bp.route('/subscription')
@login_required
def subscription_plans():
    """Show subscription plans"""
    payment_service = PaymentService()
    prices = payment_service.get_subscription_prices()
    
    current_subscription = None
    if current_user.workplace_id:
        current_subscription = Subscription.query.filter_by(
            workplace_id=current_user.workplace_id
        ).first()
    
    return render_template('premium/subscription_plans.html', 
                         prices=prices, 
                         current_subscription=current_subscription)

@premium_bp.route('/subscribe/<tier>')
@login_required
def subscribe(tier):
    """Subscribe to a tier"""
    if not current_user.workplace_id:
        flash('You must be associated with a workplace to subscribe', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    # Check master access
    if not check_master_access(current_user.email, current_user.phone_number):
        flash('Access denied. Contact the system administrator for premium access.', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    try:
        subscription_tier = SubscriptionTier(tier)
        payment_service = PaymentService()
        
        result = payment_service.initialize_payment(
            workplace_id=current_user.workplace_id,
            tier=subscription_tier,
            email=current_user.email
        )
        
        if result['status']:
            return redirect(result['authorization_url'])
        else:
            flash('Payment initialization failed. Please try again.', 'error')
    
    except ValueError:
        flash('Invalid subscription tier', 'error')
    
    return redirect(url_for('premium.subscription_plans'))

@premium_bp.route('/payment/callback')
def payment_callback():
    """Handle payment callback from Paystack"""
    reference = request.args.get('reference')
    
    if reference:
        payment_service = PaymentService()
        result = payment_service.verify_payment(reference)
        
        if result['status']:
            flash('Payment successful! Your subscription is now active.', 'success')
            return redirect(url_for('premium.subscription_plans'))
    
    flash('Payment verification failed.', 'error')
    return redirect(url_for('premium.subscription_plans'))

@premium_bp.route('/master-access')
@login_required
def master_access():
    """Master admin access management"""
    if not current_user.is_master_admin:
        flash('Access denied', 'error')
        return redirect(url_for('user.dashboard'))
    
    access_list = MasterAccess.query.all()
    return render_template('premium/master_access.html', access_list=access_list)

@premium_bp.route('/grant-access', methods=['POST'])
@login_required
def grant_access():
    """Grant master access to email/phone"""
    if not current_user.is_master_admin:
        return jsonify({'status': False, 'message': 'Access denied'})
    
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    if email:
        existing = MasterAccess.query.filter_by(email=email).first()
        if not existing:
            access = MasterAccess(
                email=email,
                phone=phone,
                created_by=current_user.email
            )
            db.session.add(access)
            db.session.commit()
            flash(f'Access granted to {email}', 'success')
        else:
            flash(f'Access already exists for {email}', 'info')
    
    return redirect(url_for('premium.master_access'))

@premium_bp.route('/chat')
@login_required
def workplace_chat():
    """Workplace chat interface"""
    if not current_user.workplace or not current_user.workplace.has_premium_feature('workplace_chat'):
        flash('This feature requires a premium subscription', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    # Get workplace chat group
    chat_group = ChatGroup.query.filter_by(
        workplace_id=current_user.workplace_id,
        chat_type=ChatType.WORKPLACE
    ).first()
    
    if not chat_group:
        # Create workplace chat group
        chat_group = ChatGroup(
            name=f"{current_user.workplace.name} General Chat",
            chat_type=ChatType.WORKPLACE,
            workplace_id=current_user.workplace_id,
            created_by=current_user.id
        )
        db.session.add(chat_group)
        db.session.commit()
    
    # Add user to chat if not already a member
    membership = ChatMember.query.filter_by(
        chat_group_id=chat_group.id,
        user_id=current_user.id
    ).first()
    
    if not membership:
        membership = ChatMember(
            chat_group_id=chat_group.id,
            user_id=current_user.id
        )
        db.session.add(membership)
        db.session.commit()
    
    messages = ChatMessage.query.filter_by(
        chat_group_id=chat_group.id
    ).order_by(ChatMessage.created_at.desc()).limit(50).all()
    
    return render_template('premium/chat.html', 
                         chat_group=chat_group, 
                         messages=messages)

@premium_bp.route('/ai-chat')
@login_required
def ai_chat():
    """AI Chatbot interface"""
    if not current_user.workplace or not current_user.workplace.has_premium_feature('ai_chatbot'):
        flash('This feature requires an Ultimate subscription', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    return render_template('premium/ai_chat.html')

@premium_bp.route('/api/ai-chat', methods=['POST'])
@login_required
def ai_chat_api():
    """AI Chatbot API endpoint"""
    if not current_user.workplace or not current_user.workplace.has_premium_feature('ai_chatbot'):
        return jsonify({'status': False, 'message': 'Premium feature required'})
    
    message = request.json.get('message')
    if not message:
        return jsonify({'status': False, 'message': 'Message required'})
    
    chatbot = AIChatbot()
    context = chatbot.get_workplace_context(current_user.workplace_id)
    response = chatbot.get_response(message, context)
    
    return jsonify(response)

@premium_bp.route('/tasks')
@login_required
def task_management():
    """Task management interface"""
    if not current_user.workplace or not current_user.workplace.has_premium_feature('task_management'):
        flash('This feature requires an Enterprise or Ultimate subscription', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    tasks = Task.query.filter_by(workplace_id=current_user.workplace_id).all()
    return render_template('premium/tasks.html', tasks=tasks)

@premium_bp.route('/library')
@login_required
def library():
    """Library management interface"""
    if not current_user.workplace or not current_user.workplace.has_premium_feature('library_management'):
        flash('This feature requires an Ultimate subscription', 'error')
        return redirect(url_for('premium.subscription_plans'))
    
    library_items = LibraryItem.query.filter_by(
        workplace_id=current_user.workplace_id
    ).all()
    
    return render_template('premium/library.html', library_items=library_items)
