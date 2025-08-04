import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.islands import islands_bp
from src.routes.activities import activities_bp
from src.routes.activity_1 import activity_1_bp
from src.routes.activity_2 import activity_2_bp
from src.routes.gamification import gamification_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'utopai-secret-key-2024-super-secure'

# CORS configuration for production
allowed_origins = os.environ.get('ALLOWED_ORIGINS')
if allowed_origins:
    # Production: Use specific origins
    origins = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, 
         supports_credentials=True,
         origins=origins,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
else:
    # Development: Allow all origins
    CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(islands_bp, url_prefix='/api')
app.register_blueprint(activities_bp, url_prefix='/api')
app.register_blueprint(activity_1_bp, url_prefix='/api')
app.register_blueprint(activity_2_bp, url_prefix='/api')
app.register_blueprint(gamification_bp, url_prefix='/api/gamification')

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production: Use PostgreSQL from Railway
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development: Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database and seed data
with app.app_context():
    db.create_all()
    
    # Seed initial data if not exists
    from src.models.user import Island, Activity
    
    if Island.query.count() == 0:
        # Create Ø 1: ChatGPT og Prompting
        island1 = Island(
            name="Prompt City",
            description="Lær at mestre ChatGPT og prompting!",
            order_number=1,
            unlock_requirement=0
        )
        db.session.add(island1)
        db.session.commit()
        
        # Create sample activities for Ø 1
        activities = [
            Activity(
                island_id=island1.id,
                name="Hvad er ChatGPT?",
                description="Lær grundlæggende om AI og ChatGPT",
                activity_type="intro",
                order_number=1,
                points_reward=50,
                difficulty_level=1
            ),
            Activity(
                island_id=island1.id,
                name="Dit første prompt",
                description="Skriv dit første prompt til ChatGPT",
                activity_type="prompt_builder",
                order_number=2,
                points_reward=100,
                difficulty_level=1
            ),
            Activity(
                island_id=island1.id,
                name="Klare vs. uklare prompts",
                description="Lær forskellen på gode og dårlige prompts",
                activity_type="quiz",
                order_number=3,
                points_reward=75,
                difficulty_level=2
            ),
            Activity(
                island_id=island1.id,
                name="Chat med AI-mentoren",
                description="Øv dig i at chatte med AI",
                activity_type="chat",
                order_number=4,
                points_reward=150,
                difficulty_level=2
            ),
            Activity(
                island_id=island1.id,
                name="Kreativ prompt-udfordring",
                description="Lav dit mest kreative prompt!",
                activity_type="creative",
                order_number=5,
                points_reward=200,
                difficulty_level=3
            )
        ]
        
        for activity in activities:
            db.session.add(activity)
        
        db.session.commit()
        print("Database seeded with initial data!")
    
    # Seed badges
    from src.routes.gamification import seed_badges
    seed_badges()

# Health check endpoint for Railway
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'UTOPAI Backend'}, 200

# Serve static files and handle SPA routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # If path is empty, return API info
    if path == '':
        return {'message': 'UTOPAI Backend API', 'status': 'running'}, 200
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

