from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Activity, UserProgress
from src.services.openai_service import openai_service
from datetime import datetime
import json

activity_1_bp = Blueprint('activity_1', __name__)

def require_child_auth():
    """Decorator to require child authentication"""
    if 'user_id' not in session or session.get('user_type') != 'child':
        return jsonify({'error': 'Child authentication required'}), 401
    return None

@activity_1_bp.route('/activity/1/start', methods=['POST'])
def start_activity_1():
    """Start Aktivitet 1: Hvad er ChatGPT?"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        # Get activity 1
        activity = Activity.query.filter_by(
            title="Hvad er ChatGPT?",
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
        intro_content = openai_service.generate_activity_1_intro(user.chosen_theme)
        
        return jsonify({
            'activity': activity.to_dict(),
            'progress': progress.to_dict(),
            'intro_content': intro_content,
            'user_theme': user.chosen_theme,
            'steps': [
                {
                    'id': 1,
                    'title': 'Introduktion til AI og ChatGPT',
                    'type': 'interactive_story',
                    'duration': 10
                },
                {
                    'id': 2,
                    'title': 'Sådan "tænker" ChatGPT',
                    'type': 'visualization',
                    'duration': 15
                },
                {
                    'id': 3,
                    'title': 'ChatGPT\'s superkræfter og begrænsninger',
                    'type': 'card_game',
                    'duration': 15
                }
            ]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@activity_1_bp.route('/activity/1/step/<int:step_id>', methods=['GET'])
def get_activity_1_step(step_id):
    """Get specific step content for Activity 1"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if step_id == 1:
            # Step 1: Interactive story introduction
            content = openai_service.generate_interactive_story(user.chosen_theme)
            return jsonify({
                'step': {
                    'id': 1,
                    'title': 'Introduktion til AI og ChatGPT',
                    'type': 'interactive_story',
                    'content': content
                }
            }), 200
            
        elif step_id == 2:
            # Step 2: How ChatGPT "thinks"
            content = {
                'explanation': openai_service.generate_thinking_explanation(user.chosen_theme),
                'word_chain_game': openai_service.generate_word_chain_game(user.chosen_theme),
                'comparison': openai_service.generate_chatgpt_vs_google(user.chosen_theme)
            }
            return jsonify({
                'step': {
                    'id': 2,
                    'title': 'Sådan "tænker" ChatGPT',
                    'type': 'visualization',
                    'content': content
                }
            }), 200
            
        elif step_id == 3:
            # Step 3: Superpowers and limitations
            content = {
                'superpower_cards': openai_service.generate_superpower_cards(user.chosen_theme),
                'weakness_cards': openai_service.generate_weakness_cards(user.chosen_theme),
                'quiz_questions': openai_service.generate_capability_quiz(user.chosen_theme)
            }
            return jsonify({
                'step': {
                    'id': 3,
                    'title': 'ChatGPT\'s superkræfter og begrænsninger',
                    'type': 'card_game',
                    'content': content
                }
            }), 200
        
        else:
            return jsonify({'error': 'Step not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@activity_1_bp.route('/activity/1/step/<int:step_id>/submit', methods=['POST'])
def submit_activity_1_step(step_id):
    """Submit answer for a specific step in Activity 1"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        data = request.get_json()
        
        # Get activity and progress
        activity = Activity.query.filter_by(
            title="Hvad er ChatGPT?",
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
            # Interactive story completion
            story_choices = data.get('choices', [])
            result = openai_service.evaluate_story_choices(story_choices, user.chosen_theme)
            points_earned = 20
            
        elif step_id == 2:
            # Word chain game and comparison
            word_chain_answer = data.get('word_chain', [])
            comparison_answer = data.get('comparison', '')
            
            result = openai_service.evaluate_thinking_exercises(
                word_chain_answer, 
                comparison_answer, 
                user.chosen_theme
            )
            points_earned = 30
            
        elif step_id == 3:
            # Card game and quiz
            card_answers = data.get('card_sorting', {})
            quiz_answers = data.get('quiz_answers', [])
            
            result = openai_service.evaluate_capability_understanding(
                card_answers, 
                quiz_answers, 
                user.chosen_theme
            )
            points_earned = 40
        
        # Update progress
        current_step_data = progress.step_data or {}
        current_step_data[f'step_{step_id}'] = {
            'completed': True,
            'score': result.get('score', 0),
            'timestamp': datetime.utcnow().isoformat()
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

@activity_1_bp.route('/activity/1/hint', methods=['POST'])
def get_activity_1_hint():
    """Get hint for Activity 1"""
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
        
        hint = openai_service.get_activity_1_hint(
            step_id, 
            question, 
            attempt_number, 
            user.chosen_theme
        )
        
        return jsonify({'hint': hint}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

