#!/usr/bin/env python3
import os
import sys

# Add the current directory to the path for Railway deployment
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the Flask app
from src.main import app

if __name__ == '__main__':
    # Railway provides PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Starting UTOPAI Backend on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

