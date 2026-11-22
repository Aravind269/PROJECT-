"""
Community Renewable Energy Portal - Main Root Launcher
Imports and runs the Flask application from the backend package.
"""
import sys
import os

# Add backend directory to sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    print("[*] Starting Community Renewable Energy Awareness and Management Portal...")
    print("[*] Server running at: http://localhost:5000 (Press Ctrl+C to stop)")
    app.run(host='0.0.0.0', port=5000, debug=True)
