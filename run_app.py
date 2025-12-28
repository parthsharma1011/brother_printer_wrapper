#!/usr/bin/env python3
import os
import sys

# Add the webapp directory to Python path
sys.path.insert(0, '/Users/parthsharma/Desktop/brother_printer/webapp')

# Set environment variables
os.environ['PORT'] = '8080'
os.environ['HOST'] = '127.0.0.1'

# Import and run the app
import app

if __name__ == '__main__':
    print("🚀 Starting on port 8080...")
    app.app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)