#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Brother QL-700 Label Printer</h1><p>Server is working!</p>'

if __name__ == '__main__':
    print('🚀 Starting test server...')
    print('📡 Open: http://127.0.0.1:5000')
    print('Press Ctrl+C to stop')
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)