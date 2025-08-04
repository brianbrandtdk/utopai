from flask import Blueprint, jsonify
from src.models.user import db, User
from datetime import date

init_db_bp = Blueprint('init_db', __name__)

@init_db_bp.route('/init-database', methods=['POST'])
def init_database():
    """Initialize database with test users"""
    try:
        # Check if users already exist
        if User.query.filter_by(email='superhelt@utopai.dk').first():
            return jsonify({'message': 'Test users already exist'}), 200
        
        # Create test users
        test_users = [
            User(
                username="superhelt_barn",
                email="superhelt@utopai.dk",
                date_of_birth=date(2015, 1, 1),
                chosen_theme="superhelte",
                total_points=250,
                current_island=1
            ),
            User(
                username="prinsesse_barn",
                email="prinsesse@utopai.dk",
                date_of_birth=date(2016, 6, 15),
                chosen_theme="prinsesse",
                total_points=180,
                current_island=1
            )
        ]
        
        for user in test_users:
            user.set_password("password123")
            db.session.add(user)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Database initialized successfully',
            'users_created': len(test_users)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

