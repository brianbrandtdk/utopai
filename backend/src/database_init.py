#!/usr/bin/env python3
"""
Database initialization and seeding script for UTOPAI
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.models.user import db, Island, Activity, User, Badge

def init_database():
    """Initialize database with tables and seed data"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Seed initial data if not exists
        if Island.query.count() == 0:
            print("Seeding islands...")
            
            # Create Ø 1: ChatGPT og Prompting
            island1 = Island(
                name="Prompt City",
                description="Lær at mestre ChatGPT og prompting!",
                order_number=1,
                unlock_requirement=0
            )
            db.session.add(island1)
            db.session.commit()
            
            print("Seeding activities...")
            
            # Activities for Ø 1
            activities = [
                Activity(
                    title="Hvad er ChatGPT?",
                    description="Lær grundlæggende om ChatGPT og kunstig intelligens",
                    activity_type="intro",
                    island_id=island1.id,
                    order_number=1,
                    points_reward=100
                ),
                Activity(
                    title="Dit første prompt",
                    description="Lær at skrive dine første prompts til ChatGPT",
                    activity_type="prompt_builder",
                    island_id=island1.id,
                    order_number=2,
                    points_reward=150
                ),
                Activity(
                    title="Klare vs. uklare prompts",
                    description="Forstå forskellen på gode og dårlige prompts",
                    activity_type="quiz",
                    island_id=island1.id,
                    order_number=3,
                    points_reward=120
                ),
                Activity(
                    title="Chat med AI-mentoren",
                    description="Øv dig i at have samtaler med AI",
                    activity_type="chat",
                    island_id=island1.id,
                    order_number=4,
                    points_reward=180
                ),
                Activity(
                    title="Kreativ prompt-udfordring",
                    description="Brug din kreativitet til at lave spændende prompts",
                    activity_type="creative",
                    island_id=island1.id,
                    order_number=5,
                    points_reward=200
                )
            ]
            
            for activity in activities:
                db.session.add(activity)
            
            db.session.commit()
            
        # Seed badges if not exists
        if Badge.query.count() == 0:
            print("Seeding badges...")
            
            badges = [
                # Beginner badges
                Badge(name="Første Skridt", description="Færdiggjorde din første aktivitet", icon="🌟", requirement_type="activity_count", requirement_value=1, theme="both"),
                Badge(name="Prompt Nybegynder", description="Skrev dit første prompt", icon="✏️", requirement_type="activity_type", requirement_value="prompt_builder", theme="both"),
                Badge(name="AI Ven", description="Havde din første samtale med AI", icon="🤖", requirement_type="activity_type", requirement_value="chat", theme="both"),
                
                # Progress badges
                Badge(name="Ø Mester", description="Færdiggjorde alle aktiviteter på en ø", icon="🏝️", requirement_type="island_complete", requirement_value=1, theme="both"),
                Badge(name="Point Samler", description="Samlede 500 point", icon="💎", requirement_type="points", requirement_value=500, theme="both"),
                Badge(name="Dedikeret Lærer", description="Samlede 1000 point", icon="🎓", requirement_type="points", requirement_value=1000, theme="both"),
                
                # Theme-specific badges
                Badge(name="Superhelt Rekrut", description="Startede superhelte eventyret", icon="🦸‍♂️", requirement_type="theme_selection", requirement_value="superhelte", theme="superhelte"),
                Badge(name="Prinsesse Eventyrer", description="Startede prinsesse eventyret", icon="👸", requirement_type="theme_selection", requirement_value="prinsesse", theme="prinsesse"),
                
                # Advanced badges
                Badge(name="Prompt Mester", description="Skrev 10 høj-kvalitets prompts", icon="🎯", requirement_type="prompt_quality", requirement_value=10, theme="both"),
                Badge(name="AI Ekspert", description="Færdiggjorde alle aktiviteter på Ø 1", icon="🧠", requirement_type="island_complete", requirement_value=1, theme="both"),
                Badge(name="Kreativ Tænker", description="Færdiggjorde kreative udfordringer", icon="🎨", requirement_type="activity_type", requirement_value="creative", theme="both")
            ]
            
            for badge in badges:
                db.session.add(badge)
            
            db.session.commit()
            
        # Create test users if not exists
        if User.query.count() == 0:
            print("Creating test users...")
            
            from datetime import date
            
            test_users = [
                User(
                    username="superhelt_barn",
                    email="superhelt@utopai.dk",
                    date_of_birth=date(2015, 1, 1),  # 8 years old
                    chosen_theme="superhelte",
                    total_points=250,
                    current_island=1
                ),
                User(
                    username="prinsesse_barn",
                    email="prinsesse@utopai.dk",
                    date_of_birth=date(2016, 6, 15),  # 7 years old
                    chosen_theme="prinsesse",
                    total_points=180,
                    current_island=1
                )
            ]
            
            for user in test_users:
                user.set_password("password123")  # Use the proper password hashing method
                db.session.add(user)
            
            db.session.commit()
            
        print("Database initialization complete!")
        print(f"Islands: {Island.query.count()}")
        print(f"Activities: {Activity.query.count()}")
        print(f"Badges: {Badge.query.count()}")
        print(f"Users: {User.query.count()}")

if __name__ == '__main__':
    init_database()

