#!/usr/bin/env python3
"""
Brother QL-700 Label Printer Web Interface
A Flask web application for printing labels with QR codes
"""

import os
import io
import csv
import threading
import base64
import logging
import webbrowser
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Import print utilities
try:
    from . import print_utils
except ImportError:
    import print_utils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config.update({
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,  # 5MB upload limit
    'UPLOAD_FOLDER': os.path.join(os.path.dirname(__file__), 'uploads'),
    'SAMPLE_FOLDER': os.path.join(os.path.dirname(__file__), 'defaults'),
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
})

# Create required directories
for folder in [app.config['UPLOAD_FOLDER'], app.config['SAMPLE_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Security settings
ALLOWED_EXTENSIONS = {'csv'}
MAX_ROWS_PREVIEW = 1000
MAX_PRINT_BATCH = 10000

# Application state
app_logs = []
job_status = {'running': False, 'progress': 0, 'total': 0, 'start_time': None}
log_lock = threading.Lock()


def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def log_message(message, level='info'):
    """Thread-safe logging with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    with log_lock:
        app_logs.append(log_entry)
        # Keep only last 200 log entries
        if len(app_logs) > 200:
            app_logs.pop(0)
    
    logger.info(message)


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Brother QL-700 Label Printer'})


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and return column information"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Ensure unique filename
        base, ext = os.path.splitext(filename)
        counter = 1
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        log_message(f"File uploaded: {filename}")
        
        # Parse CSV and extract columns
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []
                
                if not fieldnames:
                    raise ValueError("No column headers found")
                
                # Count rows for validation
                row_count = sum(1 for _ in reader)
                
                if row_count > MAX_ROWS_PREVIEW:
                    log_message(f"Large CSV detected: {row_count} rows", 'warning')
        
        except Exception as e:
            # Clean up failed upload
            try:
                os.remove(filepath)
            except OSError:
                pass
            return jsonify({'error': f'Invalid CSV file: {str(e)}'}), 400
        
        return jsonify({
            'path': filepath,
            'columns': fieldnames,
            'rows': row_count
        })
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': 'Upload failed'}), 500


@app.route('/use-sample', methods=['GET'])
def use_sample():
    """Load sample CSV data for testing"""
    try:
        sample_file = os.path.join(app.config['SAMPLE_FOLDER'], 'sample.csv')
        
        if not os.path.exists(sample_file):
            return jsonify({'error': 'Sample data not available'}), 404
        
        with open(sample_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            row_count = sum(1 for _ in reader)
        
        log_message("Sample data loaded")
        
        return jsonify({
            'path': sample_file,
            'columns': fieldnames,
            'rows': row_count
        })
    
    except Exception as e:
        logger.error(f"Sample data error: {e}")
        return jsonify({'error': 'Failed to load sample data'}), 500


@app.route('/preview', methods=['POST'])
def preview():
    """Generate label preview image"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        filepath = data.get('path')
        columns = data.get('columns', [])
        include_qr = bool(data.get('qr', True))
        
        # Validate inputs
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'CSV file not found'}), 400
        
        if not columns:
            return jsonify({'error': 'No columns selected'}), 400
        
        # Read first valid row
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                return jsonify({'error': 'Invalid CSV format'}), 400
            
            # Validate columns exist
            for col in columns:
                if col not in reader.fieldnames:
                    return jsonify({'error': f'Column "{col}" not found'}), 400
            
            # Find first non-empty row
            preview_data = None
            for row in reader:
                values = [str(row.get(col, '')).strip() for col in columns]
                if any(values):
                    preview_data = ' - '.join(filter(None, values))
                    break
            
            if not preview_data:
                return jsonify({'error': 'No data found in selected columns'}), 400
        
        # Generate preview image
        img = print_utils.create_label_image_preview(preview_data, qr_enabled=include_qr)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('ascii')
        
        log_message(f"Preview generated for: {preview_data[:50]}...")
        
        return jsonify({'image_base64': img_base64})
    
    except Exception as e:
        logger.error(f"Preview error: {e}")
        return jsonify({'error': 'Preview generation failed'}), 500


@app.route('/printers', methods=['GET'])
def detect_printers():
    """Detect available Brother QL printers"""
    try:
        printers = print_utils.discover_printers()
        log_message(f"Detected {len(printers)} printer(s)")
        return jsonify({'printers': printers})
    
    except Exception as e:
        logger.error(f"Printer detection error: {e}")
        return jsonify({'printers': [], 'error': str(e)})


@app.route('/status', methods=['GET'])
def get_status():
    """Get current job status and recent logs"""
    with log_lock:
        recent_logs = app_logs[-50:]  # Last 50 log entries
    
    return jsonify({
        'job': job_status,
        'logs': recent_logs
    })


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large (max 5MB)'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500


def open_browser(url):
    """Open browser after a short delay"""
    import time
    time.sleep(1.5)  # Wait for server to start
    try:
        webbrowser.open(url)
        print(f"🌐 Opened browser: {url}")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"📱 Please open manually: {url}")


if __name__ == '__main__':
    # Configuration from environment variables
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    url = f"http://{host}:{port}"
    
    print("🏷️  Brother QL-700 Label Printer Web Interface")
    print("=" * 50)
    print(f"🚀 Starting server...")
    print(f"📡 URL: {url}")
    print(f"🔧 Debug: Disabled (production mode)")
    print("=" * 50)
    print("📋 Features:")
    print("   • CSV upload and column selection")
    print("   • Live label preview with QR codes")
    print("   • Automatic printer detection")
    print("   • Real-time progress tracking")
    print("=" * 50)
    print("Press Ctrl+C to stop")
    print()
    
    # Open browser automatically
    if not os.environ.get('NO_BROWSER'):
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    
    try:
        app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print("💡 Try running: pip install flask")