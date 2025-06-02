import openai
from flask import current_app
import json

class AIChatbot:
    def __init__(self):
        openai.api_key = current_app.config.get('OPENAI_API_KEY')
        self.system_prompt = """
        You are a helpful AI assistant for a Workplace Management System. You can help users with:
        
        1. Seat booking and management
        2. Workplace navigation and features
        3. Task management and scheduling
        4. General workplace productivity tips
        5. System usage and troubleshooting
        
        Always be professional, helpful, and concise in your responses.
        If you don't know something specific about the system, suggest contacting support.
        """
    
    def get_response(self, user_message, context=None):
        """Get AI response to user message"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                'status': True,
                'message': response.choices[0].message.content.strip()
            }
        
        except Exception as e:
            return {
                'status': False,
                'message': "I'm sorry, I'm having trouble responding right now. Please try again later."
            }
    
    def get_workplace_context(self, workplace_id):
        """Get workplace-specific context for better responses"""
        from models.workplace import Workplace
        from models.hall import Hall
        
        workplace = Workplace.query.get(workplace_id)
        if workplace:
            halls = Hall.query.filter_by(workplace_id=workplace_id).count()
            return f"Workplace: {workplace.name}, Halls: {halls}"
        return None
