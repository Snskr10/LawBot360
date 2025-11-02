from flask import Blueprint, request, jsonify
from config import Config
import json

bp = Blueprint('chat', __name__)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

def get_openai_client():
    """Get or create OpenAI client"""
    if not OPENAI_AVAILABLE:
        return None
    
    api_key = Config.OPENAI_API_KEY
    if not api_key:
        return None
    
    try:
        return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"OpenAI client initialization failed: {e}")
        return None

@bp.route('/', methods=['POST'])
def chat():
    """Chat endpoint that works like ChatGPT with conversation history"""
    try:
        openai_client = get_openai_client()
        
        if not openai_client:
            return jsonify({
                'error': 'OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables or .env file.'
            }), 503
        
        data = request.json
        messages = data.get('messages', [])
        user_message = data.get('message', '')
        
        # Build conversation history
        conversation_messages = [
            {
                "role": "system",
                "content": """You are LawBot 360, an AI-powered legal assistant specializing in Indian laws. 
You provide educational information about legal matters, rights, and procedures related to Indian law.
You are helpful, clear, and always remind users that you provide educational information only, not legal advice.
Always recommend consulting a qualified lawyer for specific legal matters.
Keep responses conversational, clear, and easy to understand."""
            }
        ]
        
        # Add conversation history
        for msg in messages:
            if msg.get('role') == 'user':
                conversation_messages.append({"role": "user", "content": msg.get('content', '')})
            elif msg.get('role') == 'assistant':
                conversation_messages.append({"role": "assistant", "content": msg.get('content', '')})
        
        # Add current user message
        if user_message:
            conversation_messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for better performance and cost
            messages=conversation_messages,
            temperature=0.7,
            max_tokens=2000,
            stream=False
        )
        
        ai_response = response.choices[0].message.content
        
        return jsonify({
            'message': ai_response,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
        }), 200
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        if 'api_key' in error_msg.lower() or 'authentication' in error_msg.lower():
            error_msg = 'OpenAI API key is invalid or missing. Please check your configuration.'
        elif 'rate limit' in error_msg.lower():
            error_msg = 'OpenAI API rate limit exceeded. Please try again later.'
        elif 'insufficient_quota' in error_msg.lower():
            error_msg = 'OpenAI API quota exceeded. Please check your OpenAI account billing.'
        
        return jsonify({
            'error': error_msg,
            'details': traceback.format_exc() if Config.DEBUG else None
        }), 500

