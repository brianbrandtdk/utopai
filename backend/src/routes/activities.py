from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Activity, UserProgress, Island
from src.services.openai_service import openai_service
from datetime import datetime
import json

activities_bp = Blueprint('activities', __name__)

def require_child_auth():
    """Decorator to require child authentication"""
    if 'user_id' not in session or session.get('user_type') != 'child':
        return jsonify({'error': 'Child authentication required'}), 401
    return None

@activities_bp.route('/islands/<int:island_id>/activities', methods=['GET'])
def get_island_activities(island_id):
    """Get all activities for an island"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Get island
        island = Island.query.get(island_id)
        if not island:
            return jsonify({'error': 'Island not found'}), 404
        
        # Get activities for island
        activities = Activity.query.filter_by(
            island_id=island_id, 
            is_active=True
        ).order_by(Activity.order_number).all()
        
        # Get user progress for each activity
        activities_with_progress = []
        for activity in activities:
            progress = UserProgress.query.filter_by(
                user_id=user_id,
                activity_id=activity.id
            ).first()
            
            activity_data = activity.to_dict()
            activity_data['progress'] = progress.to_dict() if progress else {
                'status': 'not_started',
                'score': None,
                'attempts': 0
            }
            
            activities_with_progress.append(activity_data)
        
        return jsonify({
            'island': island.to_dict(),
            'activities': activities_with_progress,
            'user_theme': user.chosen_theme
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<int:activity_id>/start', methods=['POST'])
def start_activity(activity_id):
    """Start an activity"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Get activity
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Get or create progress
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                activity_id=activity_id,
                status='in_progress'
            )
            db.session.add(progress)
        else:
            progress.status = 'in_progress'
        
        db.session.commit()
        
        # Generate dynamic content based on activity type
        content = None
        if activity.activity_type in ['quiz', 'prompt_builder', 'creative']:
            content = openai_service.generate_activity_content(
                activity.activity_type,
                user.chosen_theme,
                activity.difficulty_level
            )
        
        return jsonify({
            'activity': activity.to_dict(),
            'progress': progress.to_dict(),
            'content': content,
            'user_theme': user.chosen_theme
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<int:activity_id>/submit', methods=['POST'])
def submit_activity_answer(activity_id):
    """Submit answer for an activity"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        # Get activity and progress
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id
        ).first()
        
        if not progress:
            return jsonify({'error': 'Activity not started'}), 400
        
        # Increment attempts
        progress.attempts += 1
        
        # Process answer based on activity type
        result = {}
        
        if activity.activity_type == 'quiz':
            correct_answer = data.get('correct_answer')
            user_answer = data.get('answer')
            
            is_correct = user_answer == correct_answer
            score = 100 if is_correct else max(0, 100 - (progress.attempts - 1) * 20)
            
            result = {
                'correct': is_correct,
                'score': score,
                'feedback': "Rigtigt! Godt klaret! 🎉" if is_correct else f"Ikke helt rigtigt. Prøv igen! Du har {3 - progress.attempts} forsøg tilbage."
            }
            
            if is_correct or progress.attempts >= 3:
                progress.status = 'completed'
                progress.score = score
                progress.completed_at = datetime.utcnow()
                
                # Award points
                user.total_points += score
                
        elif activity.activity_type == 'prompt_builder':
            user_prompt = data.get('prompt', '')
            
            # Moderate content
            if not openai_service.moderate_content(user_prompt):
                return jsonify({'error': 'Upassende indhold detekteret'}), 400
            
            # Evaluate prompt
            evaluation = openai_service.evaluate_prompt(user_prompt, user.chosen_theme)
            score = evaluation['score']['total'] * 20  # Convert 1-5 to 0-100
            
            result = {
                'evaluation': evaluation,
                'score': score
            }
            
            progress.status = 'completed'
            progress.score = score
            progress.completed_at = datetime.utcnow()
            
            # Award points
            user.total_points += score
            
        elif activity.activity_type == 'chat':
            message = data.get('message', '')
            
            # Moderate content
            if not openai_service.moderate_content(message):
                return jsonify({'error': 'Upassende indhold detekteret'}), 400
            
            # Get chat history from session or create new
            chat_history = session.get(f'chat_history_{activity_id}', [])
            chat_history.append({"role": "user", "content": message})
            
            # Get AI response
            ai_response = openai_service.chat_with_ai(
                chat_history, 
                user.chosen_theme, 
                'chat'
            )
            
            chat_history.append({"role": "assistant", "content": ai_response})
            session[f'chat_history_{activity_id}'] = chat_history
            
            result = {
                'ai_response': ai_response,
                'chat_history': chat_history
            }
            
            # Award points for participation
            if len(chat_history) >= 6:  # At least 3 exchanges
                progress.status = 'completed'
                progress.score = 80
                progress.completed_at = datetime.utcnow()
                user.total_points += 80
            
        elif activity.activity_type == 'creative':
            user_prompt = data.get('prompt', '')
            
            # Moderate content
            if not openai_service.moderate_content(user_prompt):
                return jsonify({'error': 'Upassende indhold detekteret'}), 400
            
            # Evaluate creativity
            evaluation = openai_service.evaluate_prompt(user_prompt, user.chosen_theme)
            score = min(100, evaluation['score']['kreativitet'] * 25)  # Bonus for creativity
            
            result = {
                'evaluation': evaluation,
                'score': score
            }
            
            progress.status = 'completed'
            progress.score = score
            progress.completed_at = datetime.utcnow()
            
            # Award points
            user.total_points += score
        
        db.session.commit()
        
        return jsonify({
            'result': result,
            'progress': progress.to_dict(),
            'user_points': user.total_points
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<int:activity_id>/hint', methods=['POST'])
def get_activity_hint(activity_id):
    """Get hint for an activity"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        # Get progress
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id
        ).first()
        
        if not progress:
            return jsonify({'error': 'Activity not started'}), 400
        
        question = data.get('question', '')
        hint = openai_service.get_hint(question, progress.attempts, user.chosen_theme)
        
        return jsonify({'hint': hint}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/activities/<int:activity_id>/chat', methods=['POST'])
def chat_with_mentor(activity_id):
    """Chat with AI mentor during activity"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        message = data.get('message', '')
        
        # Moderate content
        if not openai_service.moderate_content(message):
            return jsonify({'error': 'Upassende indhold detekteret'}), 400
        
        # Get chat history
        chat_history = session.get(f'mentor_chat_{activity_id}', [])
        chat_history.append({"role": "user", "content": message})
        
        # Get AI response
        ai_response = openai_service.chat_with_ai(
            chat_history,
            user.chosen_theme,
            activity.activity_type
        )
        
        chat_history.append({"role": "assistant", "content": ai_response})
        session[f'mentor_chat_{activity_id}'] = chat_history
        
        return jsonify({
            'response': ai_response,
            'chat_history': chat_history
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activities_bp.route('/user/progress', methods=['GET'])
def get_user_progress():
    """Get overall user progress"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Get all progress
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()
        
        # Calculate statistics
        total_activities = Activity.query.filter_by(is_active=True).count()
        completed_activities = len([p for p in progress_records if p.status == 'completed'])
        total_score = sum([p.score for p in progress_records if p.score])
        
        # Get island progress
        island_progress = {}
        for island in Island.query.filter_by(is_active=True).all():
            island_activities = Activity.query.filter_by(island_id=island.id, is_active=True).all()
            completed_in_island = len([
                p for p in progress_records 
                if p.activity_id in [a.id for a in island_activities] and p.status == 'completed'
            ])
            
            island_progress[island.id] = {
                'total': len(island_activities),
                'completed': completed_in_island,
                'percentage': (completed_in_island / len(island_activities) * 100) if island_activities else 0
            }
        
        return jsonify({
            'user': user.to_dict(),
            'statistics': {
                'total_activities': total_activities,
                'completed_activities': completed_activities,
                'completion_percentage': (completed_activities / total_activities * 100) if total_activities else 0,
                'total_score': total_score,
                'total_points': user.total_points
            },
            'island_progress': island_progress,
            'recent_progress': [p.to_dict() for p in progress_records[-5:]]  # Last 5 activities
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

