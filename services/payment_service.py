import requests
import json
from flask import current_app
from models.subscription import Payment, Subscription, SubscriptionTier
from models.workplace import Workplace
from app import db
from datetime import datetime, timedelta

class PaymentService:
    def __init__(self):
        self.paystack_secret_key = current_app.config.get('PAYSTACK_SECRET_KEY')
        self.paystack_public_key = current_app.config.get('PAYSTACK_PUBLIC_KEY')
        self.base_url = "https://api.paystack.co"
    
    def get_subscription_prices(self):
        """Get subscription tier prices in Naira"""
        return {
            SubscriptionTier.BASIC: 5000,  # ₦5,000/month
            SubscriptionTier.PROFESSIONAL: 15000,  # ₦15,000/month
            SubscriptionTier.ENTERPRISE: 35000,  # ₦35,000/month
            SubscriptionTier.ULTIMATE: 75000,  # ₦75,000/month
        }
    
    def initialize_payment(self, workplace_id, tier, email, duration_months=1):
        """Initialize payment with Paystack"""
        prices = self.get_subscription_prices()
        amount = prices[tier] * duration_months * 100  # Convert to kobo
        
        # Create payment record
        payment = Payment(
            workplace_id=workplace_id,
            amount=amount / 100,  # Store in Naira
            currency='NGN',
            payment_method='paystack',
            reference=f"WMS_{workplace_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        db.session.add(payment)
        db.session.commit()
        
        # Initialize with Paystack
        headers = {
            'Authorization': f'Bearer {self.paystack_secret_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'email': email,
            'amount': amount,
            'reference': payment.reference,
            'callback_url': f"{current_app.config.get('BASE_URL')}/payment/callback",
            'metadata': {
                'workplace_id': workplace_id,
                'tier': tier.value,
                'duration_months': duration_months,
                'payment_id': payment.id
            }
        }
        
        response = requests.post(
            f"{self.base_url}/transaction/initialize",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status']:
                return {
                    'status': True,
                    'authorization_url': result['data']['authorization_url'],
                    'reference': payment.reference
                }
        
        return {'status': False, 'message': 'Payment initialization failed'}
    
    def verify_payment(self, reference):
        """Verify payment with Paystack"""
        headers = {
            'Authorization': f'Bearer {self.paystack_secret_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{self.base_url}/transaction/verify/{reference}",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] and result['data']['status'] == 'success':
                # Update payment record
                payment = Payment.query.filter_by(reference=reference).first()
                if payment:
                    payment.status = 'success'
                    payment.gateway_response = json.dumps(result['data'])
                    
                    # Create or update subscription
                    metadata = result['data']['metadata']
                    workplace_id = metadata['workplace_id']
                    tier = SubscriptionTier(metadata['tier'])
                    duration_months = metadata['duration_months']
                    
                    subscription = Subscription.query.filter_by(workplace_id=workplace_id).first()
                    if not subscription:
                        subscription = Subscription(workplace_id=workplace_id)
                        db.session.add(subscription)
                    
                    subscription.tier = tier
                    subscription.start_date = datetime.utcnow()
                    subscription.end_date = datetime.utcnow() + timedelta(days=30 * duration_months)
                    subscription.is_active = True
                    subscription.payment_reference = reference
                    subscription.amount_paid = payment.amount
                    
                    payment.subscription = subscription
                    
                    db.session.commit()
                    
                    return {'status': True, 'subscription': subscription}
        
        return {'status': False, 'message': 'Payment verification failed'}

def check_master_access(email, phone=None):
    """Check if user has master access to premium features"""
    from models.subscription import MasterAccess
    
    access = MasterAccess.query.filter_by(email=email, is_active=True).first()
    if access:
        return True
    
    if phone:
        access = MasterAccess.query.filter_by(phone=phone, is_active=True).first()
        return access is not None
    
    return False
