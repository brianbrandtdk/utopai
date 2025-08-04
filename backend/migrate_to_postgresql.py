#!/usr/bin/env python3
"""
Migration script to move data from SQLite to PostgreSQL
Run this after setting up PostgreSQL on Railway
"""
import os
import sys
import sqlite3
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

def export_sqlite_data():
    """Export data from SQLite database"""
    sqlite_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
    
    if not os.path.exists(sqlite_path):
        print("No SQLite database found. Starting fresh.")
        return None
    
    print(f"Exporting data from {sqlite_path}")
    
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {}
    
    # Export tables
    tables = ['users', 'islands', 'activities', 'badges', 'user_progress', 'user_badges']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            data[table] = [dict(row) for row in rows]
            print(f"Exported {len(rows)} rows from {table}")
        except sqlite3.OperationalError as e:
            print(f"Table {table} not found: {e}")
            data[table] = []
    
    conn.close()
    
    # Save to JSON file
    export_file = 'sqlite_export.json'
    with open(export_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"Data exported to {export_file}")
    return export_file

def import_to_postgresql():
    """Import data to PostgreSQL database"""
    from src.main import app
    from src.models.user import db, User, Island, Activity, Badge, UserProgress, UserBadge
    
    export_file = 'sqlite_export.json'
    
    if not os.path.exists(export_file):
        print("No export file found. Running fresh database initialization.")
        from src.database_init import init_database
        init_database()
        return
    
    print("Importing data to PostgreSQL...")
    
    with open(export_file, 'r') as f:
        data = json.load(f)
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Import islands
        for island_data in data.get('islands', []):
            island = Island(**{k: v for k, v in island_data.items() if k != 'id'})
            db.session.add(island)
        
        db.session.commit()
        
        # Import activities
        for activity_data in data.get('activities', []):
            activity = Activity(**{k: v for k, v in activity_data.items() if k != 'id'})
            db.session.add(activity)
        
        db.session.commit()
        
        # Import badges
        for badge_data in data.get('badges', []):
            badge = Badge(**{k: v for k, v in badge_data.items() if k != 'id'})
            db.session.add(badge)
        
        db.session.commit()
        
        # Import users
        for user_data in data.get('users', []):
            user = User(**{k: v for k, v in user_data.items() if k != 'id'})
            db.session.add(user)
        
        db.session.commit()
        
        # Import user progress
        for progress_data in data.get('user_progress', []):
            progress = UserProgress(**{k: v for k, v in progress_data.items() if k != 'id'})
            db.session.add(progress)
        
        # Import user badges
        for badge_data in data.get('user_badges', []):
            user_badge = UserBadge(**{k: v for k, v in badge_data.items() if k != 'id'})
            db.session.add(user_badge)
        
        db.session.commit()
        
        print("Data import complete!")
        print(f"Islands: {Island.query.count()}")
        print(f"Activities: {Activity.query.count()}")
        print(f"Badges: {Badge.query.count()}")
        print(f"Users: {User.query.count()}")

def main():
    """Main migration function"""
    print("UTOPAI Database Migration Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'export':
        export_sqlite_data()
    elif len(sys.argv) > 1 and sys.argv[1] == 'import':
        import_to_postgresql()
    else:
        print("Usage:")
        print("  python migrate_to_postgresql.py export  # Export SQLite data")
        print("  python migrate_to_postgresql.py import  # Import to PostgreSQL")

if __name__ == '__main__':
    main()

