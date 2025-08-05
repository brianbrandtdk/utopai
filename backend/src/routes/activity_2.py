from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Activity, UserProgress
from src.services.openai_service import openai_service
from datetime import datetime
import json

activity_2_bp = Blueprint('activity_2', __name__)

def require_child_auth():
    """Decorator to require child authentication"""
    if 'user_id' not in session or session.get('user_type') != 'child':
        return jsonify({'error': 'Child authentication required'}), 401
    return None

@activity_2_bp.route('/activity/2/start', methods=['POST'])
def start_activity_2():
    """Start Aktivitet 2: Dit første prompt"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Get activity 2
        activity = Activity.query.filter_by(
            name="Dit første prompt",
            island_id=1
        ).first()
        
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Get or create progress
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity.id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                activity_id=activity.id,
                status='in_progress'
            )
            db.session.add(progress)
        else:
            progress.status = 'in_progress'
        
        db.session.commit()
        
        # Generate personalized introduction based on theme
        intro_content = openai_service.generate_activity_2_intro(user.chosen_theme)
        
        return jsonify({
            'activity': activity.to_dict(),
            'progress': progress.to_dict(),
            'intro_content': intro_content,
            'user_theme': user.chosen_theme,
            'steps': [
                {
                    'id': 1,
                    'title': 'Guidet første samtale',
                    'type': 'guided_prompt',
                    'duration': 5
                },
                {
                    'id': 2,
                    'title': 'Høflighedstræning',
                    'type': 'politeness_training',
                    'duration': 5
                },
                {
                    'id': 3,
                    'title': 'Personaliseret øvelse',
                    'type': 'personalized_exercise',
                    'duration': 5
                }
            ]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/step/<int:step_id>', methods=['GET'])
def get_activity_2_step(step_id):
    """Get specific step content for Activity 2"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if step_id == 1:
            # Step 1: Guided first conversation
            content = openai_service.generate_guided_prompt_builder(user.chosen_theme)
            return jsonify({
                'step': {
                    'id': 1,
                    'title': 'Guidet første samtale',
                    'type': 'guided_prompt',
                    'content': content
                }
            }), 200
            
        elif step_id == 2:
            # Step 2: Politeness training
            content = openai_service.generate_politeness_training(user.chosen_theme)
            return jsonify({
                'step': {
                    'id': 2,
                    'title': 'Høflighedstræning',
                    'type': 'politeness_training',
                    'content': content
                }
            }), 200
            
        elif step_id == 3:
            # Step 3: Personalized exercise
            content = openai_service.generate_personalized_prompt_exercise(user.chosen_theme)
            return jsonify({
                'step': {
                    'id': 3,
                    'title': 'Personaliseret øvelse',
                    'type': 'personalized_exercise',
                    'content': content
                }
            }), 200
        
        else:
            return jsonify({'error': 'Step not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/build-prompt', methods=['POST'])
def build_prompt():
    """Interactive prompt builder endpoint"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        prompt_parts = data.get('prompt_parts', {})
        step_id = data.get('step_id', 1)
        
        # Build prompt from parts
        built_prompt = openai_service.build_prompt_from_parts(
            prompt_parts, 
            user.chosen_theme,
            step_id
        )
        
        # Get AI preview of what the response would be
        preview_response = openai_service.get_prompt_preview(
            built_prompt,
            user.chosen_theme
        )
        
        return jsonify({
            'built_prompt': built_prompt,
            'preview_response': preview_response,
            'quality_score': openai_service.evaluate_prompt_quality(built_prompt),
            'suggestions': openai_service.get_prompt_improvement_suggestions(
                built_prompt, 
                user.chosen_theme
            )
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/test-prompt', methods=['POST'])
def test_prompt():
    """Test a user's prompt with real AI"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        user_prompt = data.get('prompt', '')
        step_id = data.get('step_id', 1)
        
        # Moderate content
        if not openai_service.moderate_content(user_prompt):
            return jsonify({'error': 'Upassende indhold detekteret'}), 400
        
        # Get AI response to the prompt
        ai_response = openai_service.get_themed_ai_response(
            user_prompt,
            user.chosen_theme
        )
        
        # Evaluate the prompt
        evaluation = openai_service.evaluate_prompt_for_beginners(
            user_prompt,
            ai_response,
            user.chosen_theme
        )
        
        return jsonify({
            'user_prompt': user_prompt,
            'ai_response': ai_response,
            'evaluation': evaluation,
            'step_id': step_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/step/<int:step_id>/submit', methods=['POST'])
def submit_activity_2_step(step_id):
    """Submit answer for a specific step in Activity 2"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        # Get activity and progress
        activity = Activity.query.filter_by(
            title="Dit første prompt",
            island_id=1
        ).first()
        
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity.id
        ).first()
        
        if not progress:
            return jsonify({'error': 'Activity not started'}), 400
        
        # Process based on step
        result = {}
        points_earned = 0
        
        if step_id == 1:
            # Guided prompt building
            prompt_parts = data.get('prompt_parts', {})
            final_prompt = data.get('final_prompt', '')
            
            result = openai_service.evaluate_guided_prompt(
                prompt_parts, 
                final_prompt, 
                user.chosen_theme
            )
            points_earned = 30
            
        elif step_id == 2:
            # Politeness training
            politeness_examples = data.get('politeness_examples', [])
            politeness_quiz = data.get('politeness_quiz', [])
            
            result = openai_service.evaluate_politeness_training(
                politeness_examples, 
                politeness_quiz, 
                user.chosen_theme
            )
            points_earned = 25
            
        elif step_id == 3:
            # Personalized exercise
            personal_prompt = data.get('personal_prompt', '')
            ai_response = data.get('ai_response', '')
            
            result = openai_service.evaluate_personalized_exercise(
                personal_prompt, 
                ai_response, 
                user.chosen_theme
            )
            points_earned = 45
        
        # Update progress
        current_step_data = progress.step_data or {}
        current_step_data[f'step_{step_id}'] = {
            'completed': True,
            'score': result.get('score', 0),
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        progress.step_data = current_step_data
        
        # Check if all steps completed
        completed_steps = len([k for k in current_step_data.keys() if current_step_data[k]['completed']])
        if completed_steps >= 3:
            progress.status = 'completed'
            progress.completed_at = datetime.utcnow()
            total_score = sum([current_step_data[k]['score'] for k in current_step_data.keys()])
            progress.score = total_score
            points_earned += 50  # Completion bonus
        
        # Award points
        user.total_points += points_earned
        
        db.session.commit()
        
        return jsonify({
            'result': result,
            'points_earned': points_earned,
            'progress': progress.to_dict(),
            'user_points': user.total_points,
            'activity_completed': progress.status == 'completed'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/hint', methods=['POST'])
def get_activity_2_hint():
    """Get hint for Activity 2"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        step_id = data.get('step_id')
        question = data.get('question', '')
        attempt_number = data.get('attempt_number', 1)
        current_prompt = data.get('current_prompt', '')
        
        hint = openai_service.get_activity_2_hint(
            step_id, 
            question, 
            current_prompt,
            attempt_number, 
            user.chosen_theme
        )
        
        return jsonify({'hint': hint}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_2_bp.route('/activity/2/prompt-templates', methods=['GET'])
def get_prompt_templates():
    """Get prompt templates for beginners"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        templates = openai_service.get_beginner_prompt_templates(user.chosen_theme)
        
        return jsonify({
            'templates': templates,
            'user_theme': user.chosen_theme
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

