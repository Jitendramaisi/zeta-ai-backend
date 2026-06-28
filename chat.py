from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from google import genai
from models import db, Conversation, Message, User
import os
import logging

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Initialize Gemini client
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    client = genai.Client(api_key=api_key)
else:
    logger.warning('GEMINI_API_KEY not set')
    client = None

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message and get AI response"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data.get('message')
        conversation_id = data.get('conversation_id')
        
        # Check if client is initialized
        if not client:
            return jsonify({'error': 'AI service not configured'}), 503
        
        # Get or create conversation
        if conversation_id:
            conversation = Conversation.query.filter_by(
                id=conversation_id,
                user_id=user_id
            ).first()
            if not conversation:
                return jsonify({'error': 'Conversation not found'}), 404
        else:
            conversation = Conversation(user_id=user_id, title=user_message[:50])
            db.session.add(conversation)
            db.session.flush()
        
        # Save user message
        user_msg = Message(conversation_id=conversation.id, role='user', content=user_message)
        db.session.add(user_msg)
        db.session.flush()
        
        # Get AI response
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message
            )
            ai_reply = response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return jsonify({'error': f'AI service error: {str(e)}'}), 503
        
        # Save AI response
        ai_msg = Message(conversation_id=conversation.id, role='assistant', content=ai_reply)
        db.session.add(ai_msg)
        db.session.commit()
        
        logger.info(f"Message processed for user {user_id} in conversation {conversation.id}")
        return jsonify({
            'conversation_id': conversation.id,
            'user_message': user_message,
            'ai_reply': ai_reply,
            'messages': [m.to_dict() for m in conversation.messages]
        }), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for current user"""
    try:
        user_id = get_jwt_identity()
        conversations = Conversation.query.filter_by(user_id=user_id).order_by(
            Conversation.updated_at.desc()
        ).all()
        
        return jsonify({
            'conversations': [c.to_dict() for c in conversations]
        }), 200
    
    except Exception as e:
        logger.error(f"Get conversations error: {str(e)}")
        return jsonify({'error': f'Failed to get conversations: {str(e)}'}), 500

@chat_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    """Get specific conversation with all messages"""
    try:
        user_id = get_jwt_identity()
        conversation = Conversation.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        return jsonify({
            'conversation': conversation.to_dict(),
            'messages': [m.to_dict() for m in conversation.messages]
        }), 200
    
    except Exception as e:
        logger.error(f"Get conversation error: {str(e)}")
        return jsonify({'error': f'Failed to get conversation: {str(e)}'}), 500

@chat_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(conversation_id):
    """Delete a conversation"""
    try:
        user_id = get_jwt_identity()
        conversation = Conversation.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        db.session.delete(conversation)
        db.session.commit()
        
        logger.info(f"Conversation {conversation_id} deleted by user {user_id}")
        return jsonify({'message': 'Conversation deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Delete conversation error: {str(e)}")
        return jsonify({'error': f'Failed to delete conversation: {str(e)}'}), 500
