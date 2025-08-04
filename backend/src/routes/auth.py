from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Parent, ParentChildRelation
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new child and parent"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['child_username', 'child_email', 'child_password', 'child_date_of_birth',
                          'parent_email', 'parent_password', 'parent_first_name', 'parent_last_name']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if child username or email already exists
        if User.query.filter_by(username=data['child_username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['child_email']).first():
            return jsonify({'error': 'Child email already exists'}), 400
        
        # Check if parent email already exists
        if Parent.query.filter_by(email=data['parent_email']).first():
            return jsonify({'error': 'Parent email already exists'}), 400
        
        # Create parent
        parent = Parent(
            email=data['parent_email'],
            first_name=data['parent_first_name'],
            last_name=data['parent_last_name']
        )
        parent.set_password(data['parent_password'])
        
        # Create child
        child = User(
            username=data['child_username'],
            email=data['child_email'],
            date_of_birth=datetime.strptime(data['child_date_of_birth'], '%Y-%m-%d').date()
        )
        child.set_password(data['child_password'])
        
        # Save to database
        db.session.add(parent)
        db.session.add(child)
        db.session.commit()
        
        # Create parent-child relation
        relation = ParentChildRelation(parent_id=parent.id, child_id=child.id)
        db.session.add(relation)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'child': child.to_dict(),
            'parent': parent.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login for both children and parents"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        user_type = data.get('user_type', 'child')  # 'child' or 'parent'
        
        if user_type == 'child':
            user = User.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                session['user_id'] = user.id
                session['user_type'] = 'child'
                return jsonify({
                    'message': 'Login successful',
                    'user': user.to_dict(),
                    'user_type': 'child'
                }), 200
        
        elif user_type == 'parent':
            parent = Parent.query.filter_by(email=data['email']).first()
            if parent and parent.check_password(data['password']):
                session['user_id'] = parent.id
                session['user_type'] = 'parent'
                
                # Get children
                relations = ParentChildRelation.query.filter_by(parent_id=parent.id).all()
                children = [User.query.get(rel.child_id).to_dict() for rel in relations]
                
                return jsonify({
                    'message': 'Login successful',
                    'user': parent.to_dict(),
                    'user_type': 'parent',
                    'children': children
                }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout current user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged in user"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_type = session.get('user_type', 'child')
        user_id = session['user_id']
        
        if user_type == 'child':
            user = User.query.get(user_id)
            if user:
                return jsonify({
                    'user': user.to_dict(),
                    'user_type': 'child'
                }), 200
        
        elif user_type == 'parent':
            parent = Parent.query.get(user_id)
            if parent:
                # Get children
                relations = ParentChildRelation.query.filter_by(parent_id=parent.id).all()
                children = [User.query.get(rel.child_id).to_dict() for rel in relations]
                
                return jsonify({
                    'user': parent.to_dict(),
                    'user_type': 'parent',
                    'children': children
                }), 200
        
        return jsonify({'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/select-theme', methods=['POST'])
def select_theme():
    """Select theme for child user"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'child':
            return jsonify({'error': 'Child authentication required'}), 401
        
        data = request.get_json()
        theme = data.get('theme')
        
        if theme not in ['superhelte', 'prinsesse']:
            return jsonify({'error': 'Invalid theme. Must be "superhelte" or "prinsesse"'}), 400
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.chosen_theme = theme
        db.session.commit()
        
        return jsonify({
            'message': 'Theme selected successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

