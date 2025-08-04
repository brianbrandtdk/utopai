from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Badge, UserBadge, UserProgress, Activity, Island
from datetime import datetime
import json

gamification_bp = Blueprint('gamification', __name__)

def require_child_auth():
    """Decorator to require child authentication"""
    if 'user_id' not in session or session.get('user_type') != 'child':
        return jsonify({'error': 'Child authentication required'}), 401
    return None

@gamification_bp.route('/points/award', methods=['POST'])
def award_points():
    """Award points to a user for completing an activity"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        activity_id = data.get('activity_id')
        points = data.get('points', 0)
        
        if not activity_id:
            return jsonify({'error': 'Activity ID required'}), 400
        
        # Get user and activity
        user = User.query.get(user_id)
        activity = Activity.query.get(activity_id)
        
        if not user or not activity:
            return jsonify({'error': 'User or activity not found'}), 404
        
        # Check if user already completed this activity
        existing_progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id,
            status='completed'
        ).first()
        
        if existing_progress:
            return jsonify({'error': 'Activity already completed'}), 400
        
        # Award points
        user.total_points += points
        
        # Update or create progress record
        progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                activity_id=activity_id,
                status='completed',
                score=points,
                attempts=1,
                completed_at=datetime.utcnow()
            )
            db.session.add(progress)
        else:
            progress.status = 'completed'
            progress.score = points
            progress.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Check for new badges
        new_badges = check_and_award_badges(user)
        
        return jsonify({
            'message': 'Points awarded successfully',
            'points_awarded': points,
            'total_points': user.total_points,
            'new_badges': [badge.to_dict() for badge in new_badges]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/badges', methods=['GET'])
def get_user_badges():
    """Get all badges for the current user"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all available badges
        all_badges = Badge.query.filter(
            (Badge.theme == user.chosen_theme) | (Badge.theme.is_(None))
        ).filter_by(is_active=True).all()
        
        # Get user's earned badges
        user_badges = db.session.query(UserBadge, Badge).join(Badge).filter(
            UserBadge.user_id == user_id
        ).all()
        
        earned_badge_ids = {ub.badge_id for ub, _ in user_badges}
        
        badges_data = []
        for badge in all_badges:
            badge_dict = badge.to_dict()
            badge_dict['earned'] = badge.id in earned_badge_ids
            badge_dict['earned_at'] = None
            
            # Add earned date if user has this badge
            for user_badge, _ in user_badges:
                if user_badge.badge_id == badge.id:
                    badge_dict['earned_at'] = user_badge.earned_at.isoformat()
                    break
            
            badges_data.append(badge_dict)
        
        return jsonify({
            'badges': badges_data,
            'total_badges': len(all_badges),
            'earned_badges': len(earned_badge_ids)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the top 5 users leaderboard"""
    try:
        # Get top 5 users by points
        top_users = User.query.filter_by(is_active=True).order_by(
            User.total_points.desc()
        ).limit(5).all()
        
        leaderboard_data = []
        for i, user in enumerate(top_users, 1):
            # Get user's badge count
            badge_count = UserBadge.query.filter_by(user_id=user.id).count()
            
            # Get user's completion percentage
            total_activities = Activity.query.filter_by(is_active=True).count()
            completed_activities = UserProgress.query.filter_by(
                user_id=user.id,
                status='completed'
            ).count()
            
            completion_percentage = (completed_activities / total_activities * 100) if total_activities > 0 else 0
            
            leaderboard_data.append({
                'rank': i,
                'username': user.username,
                'theme': user.chosen_theme,
                'total_points': user.total_points,
                'badge_count': badge_count,
                'completion_percentage': round(completion_percentage, 1),
                'current_island': user.current_island
            })
        
        return jsonify({
            'leaderboard': leaderboard_data,
            'total_users': User.query.filter_by(is_active=True).count()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/progress', methods=['GET'])
def get_user_progress():
    """Get detailed progress for the current user"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all user progress
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()
        
        # Get all activities
        all_activities = Activity.query.filter_by(is_active=True).all()
        total_activities = len(all_activities)
        
        # Calculate statistics
        completed_activities = len([p for p in progress_records if p.status == 'completed'])
        in_progress_activities = len([p for p in progress_records if p.status == 'in_progress'])
        
        completion_percentage = (completed_activities / total_activities * 100) if total_activities > 0 else 0
        
        # Get island progress
        islands = Island.query.filter_by(is_active=True).order_by(Island.order_number).all()
        island_progress = {}
        
        for island in islands:
            island_activities = [a for a in all_activities if a.island_id == island.id]
            island_completed = len([
                p for p in progress_records 
                if p.status == 'completed' and any(a.id == p.activity_id for a in island_activities)
            ])
            
            island_progress[str(island.id)] = {
                'name': island.name,
                'total': len(island_activities),
                'completed': island_completed,
                'percentage': (island_completed / len(island_activities) * 100) if island_activities else 0
            }
        
        # Get recent progress (last 5 activities)
        recent_progress = UserProgress.query.filter_by(user_id=user_id).order_by(
            UserProgress.completed_at.desc().nullslast(),
            UserProgress.started_at.desc()
        ).limit(5).all()
        
        return jsonify({
            'statistics': {
                'total_points': user.total_points,
                'total_activities': total_activities,
                'completed_activities': completed_activities,
                'in_progress_activities': in_progress_activities,
                'completion_percentage': round(completion_percentage, 1),
                'current_island': user.current_island,
                'badge_count': UserBadge.query.filter_by(user_id=user_id).count()
            },
            'island_progress': island_progress,
            'recent_progress': [p.to_dict() for p in recent_progress]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gamification_bp.route('/activity/start', methods=['POST'])
def start_activity():
    """Mark an activity as started"""
    auth_error = require_child_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        activity_id = data.get('activity_id')
        
        if not activity_id:
            return jsonify({'error': 'Activity ID required'}), 400
        
        # Check if activity exists
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        # Check if already started or completed
        existing_progress = UserProgress.query.filter_by(
            user_id=user_id,
            activity_id=activity_id
        ).first()
        
        if existing_progress:
            if existing_progress.status == 'completed':
                return jsonify({'error': 'Activity already completed'}), 400
            else:
                # Update attempts
                existing_progress.attempts += 1
                existing_progress.started_at = datetime.utcnow()
        else:
            # Create new progress record
            progress = UserProgress(
                user_id=user_id,
                activity_id=activity_id,
                status='in_progress',
                attempts=1,
                started_at=datetime.utcnow()
            )
            db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Activity started successfully',
            'activity_id': activity_id,
            'status': 'in_progress'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def check_and_award_badges(user):
    """Check if user qualifies for new badges and award them"""
    new_badges = []
    
    try:
        # Get all available badges for user's theme
        available_badges = Badge.query.filter(
            (Badge.theme == user.chosen_theme) | (Badge.theme.is_(None))
        ).filter_by(is_active=True).all()
        
        # Get user's current badges
        current_badge_ids = {ub.badge_id for ub in UserBadge.query.filter_by(user_id=user.id).all()}
        
        for badge in available_badges:
            if badge.id in current_badge_ids:
                continue  # User already has this badge
            
            # Check if user qualifies for this badge
            qualifies = False
            
            if badge.requirement_type == 'points':
                qualifies = user.total_points >= badge.requirement_value
            
            elif badge.requirement_type == 'activities':
                completed_count = UserProgress.query.filter_by(
                    user_id=user.id,
                    status='completed'
                ).count()
                qualifies = completed_count >= badge.requirement_value
            
            elif badge.requirement_type == 'island':
                # Check if user completed specific island
                island_activities = Activity.query.filter_by(
                    island_id=badge.requirement_value,
                    is_active=True
                ).all()
                
                completed_island_activities = UserProgress.query.filter(
                    UserProgress.user_id == user.id,
                    UserProgress.status == 'completed',
                    UserProgress.activity_id.in_([a.id for a in island_activities])
                ).count()
                
                qualifies = completed_island_activities == len(island_activities)
            
            elif badge.requirement_type == 'streak':
                # For now, just award based on consecutive days (simplified)
                qualifies = user.total_points >= badge.requirement_value * 10
            
            if qualifies:
                # Award the badge
                user_badge = UserBadge(
                    user_id=user.id,
                    badge_id=badge.id,
                    earned_at=datetime.utcnow()
                )
                db.session.add(user_badge)
                new_badges.append(badge)
        
        if new_badges:
            db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print(f"Error checking badges: {e}")
    
    return new_badges

# Seed badges data
def seed_badges():
    """Seed initial badges data"""
    try:
        if Badge.query.count() > 0:
            return  # Already seeded
        
        badges_data = [
            # Universal badges (both themes)
            {
                'name': 'Første Skridt',
                'description': 'Fuldfør din første aktivitet',
                'icon': '🎯',
                'requirement_type': 'activities',
                'requirement_value': 1,
                'theme': None
            },
            {
                'name': 'AI Nybegynder',
                'description': 'Saml 100 point',
                'icon': '⭐',
                'requirement_type': 'points',
                'requirement_value': 100,
                'theme': None
            },
            {
                'name': 'Prompt Mester',
                'description': 'Fuldfør Ø 1: ChatGPT & Prompting',
                'icon': '🏆',
                'requirement_type': 'island',
                'requirement_value': 1,
                'theme': None
            },
            {
                'name': 'Dedikeret Lærer',
                'description': 'Fuldfør 10 aktiviteter',
                'icon': '📚',
                'requirement_type': 'activities',
                'requirement_value': 10,
                'theme': None
            },
            {
                'name': 'Point Samler',
                'description': 'Saml 500 point',
                'icon': '💎',
                'requirement_type': 'points',
                'requirement_value': 500,
                'theme': None
            },
            
            # Superhelte theme badges
            {
                'name': 'Superhelt Rekrut',
                'description': 'Velkommen til superhelte akademiet!',
                'icon': '🦸‍♂️',
                'requirement_type': 'points',
                'requirement_value': 50,
                'theme': 'superhelte'
            },
            {
                'name': 'AI Beskytter',
                'description': 'Beskyt verden med AI viden',
                'icon': '🛡️',
                'requirement_type': 'activities',
                'requirement_value': 5,
                'theme': 'superhelte'
            },
            {
                'name': 'Cyber Helt',
                'description': 'Mester af digital teknologi',
                'icon': '⚡',
                'requirement_type': 'points',
                'requirement_value': 300,
                'theme': 'superhelte'
            },
            
            # Prinsesse theme badges
            {
                'name': 'Kongelig Lærling',
                'description': 'Velkommen til det magiske kongerige!',
                'icon': '👸',
                'requirement_type': 'points',
                'requirement_value': 50,
                'theme': 'prinsesse'
            },
            {
                'name': 'Magisk Viden',
                'description': 'Lær AI-magi at kende',
                'icon': '✨',
                'requirement_type': 'activities',
                'requirement_value': 5,
                'theme': 'prinsesse'
            },
            {
                'name': 'Krystal Mester',
                'description': 'Behersker de magiske krystaller',
                'icon': '💎',
                'requirement_type': 'points',
                'requirement_value': 300,
                'theme': 'prinsesse'
            }
        ]
        
        for badge_data in badges_data:
            badge = Badge(**badge_data)
            db.session.add(badge)
        
        db.session.commit()
        print("Badges seeded successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding badges: {e}")

