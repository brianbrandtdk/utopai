from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Island, Activity, UserProgress

islands_bp = Blueprint('islands', __name__)

@islands_bp.route('/islands', methods=['GET'])
def get_islands():
    """Get all islands for current user"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'child':
            return jsonify({'error': 'Child authentication required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        islands = Island.query.filter_by(is_active=True).order_by(Island.order_number).all()
        
        islands_data = []
        for island in islands:
            # Check if island is unlocked
            is_unlocked = user.total_points >= island.unlock_requirement
            
            # Get activities for this island
            activities = Activity.query.filter_by(island_id=island.id, is_active=True).order_by(Activity.order_number).all()
            
            # Get user progress for activities
            activities_data = []
            for activity in activities:
                progress = UserProgress.query.filter_by(user_id=user.id, activity_id=activity.id).first()
                activity_data = activity.to_dict()
                activity_data['progress'] = progress.to_dict() if progress else None
                activities_data.append(activity_data)
            
            island_data = island.to_dict()
            island_data['is_unlocked'] = is_unlocked
            island_data['activities'] = activities_data
            islands_data.append(island_data)
        
        return jsonify({
            'islands': islands_data,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@islands_bp.route('/islands/<int:island_id>/activities', methods=['GET'])
def get_island_activities(island_id):
    """Get activities for specific island"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'child':
            return jsonify({'error': 'Child authentication required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        island = Island.query.get(island_id)
        if not island:
            return jsonify({'error': 'Island not found'}), 404
        
        # Check if island is unlocked
        if user.total_points < island.unlock_requirement:
            return jsonify({'error': 'Island not unlocked'}), 403
        
        activities = Activity.query.filter_by(island_id=island_id, is_active=True).order_by(Activity.order_number).all()
        
        activities_data = []
        for activity in activities:
            progress = UserProgress.query.filter_by(user_id=user.id, activity_id=activity.id).first()
            activity_data = activity.to_dict()
            activity_data['progress'] = progress.to_dict() if progress else None
            activities_data.append(activity_data)
        
        return jsonify({
            'island': island.to_dict(),
            'activities': activities_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@islands_bp.route('/activities/<int:activity_id>/start', methods=['POST'])
def start_activity(activity_id):
    """Start an activity"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'child':
            return jsonify({'error': 'Child authentication required'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Check if island is unlocked
        island = Island.query.get(activity.island_id)
        if user.total_points < island.unlock_requirement:
            return jsonify({'error': 'Island not unlocked'}), 403
        
        # Get or create progress
        progress = UserProgress.query.filter_by(user_id=user.id, activity_id=activity_id).first()
        if not progress:
            progress = UserProgress(user_id=user.id, activity_id=activity_id)
            db.session.add(progress)
        
        progress.status = 'in_progress'
        progress.attempts += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Activity started',
            'activity': activity.to_dict(),
            'progress': progress.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@islands_bp.route('/activities/<int:activity_id>/complete', methods=['POST'])
def complete_activity(activity_id):
    """Complete an activity"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'child':
            return jsonify({'error': 'Child authentication required'}), 401
        
        data = request.get_json()
        score = data.get('score', 0)
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Get progress
        progress = UserProgress.query.filter_by(user_id=user.id, activity_id=activity_id).first()
        if not progress:
            return jsonify({'error': 'Activity not started'}), 400
        
        # Update progress
        progress.status = 'completed'
        progress.score = score
        progress.completed_at = db.func.now()
        
        # Award points
        points_earned = activity.points_reward
        user.total_points += points_earned
        
        db.session.commit()
        
        return jsonify({
            'message': 'Activity completed',
            'points_earned': points_earned,
            'total_points': user.total_points,
            'progress': progress.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

