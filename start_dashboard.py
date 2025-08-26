#!/usr/bin/env python3
"""
Start the web dashboard
"""

from src.dashboard.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)