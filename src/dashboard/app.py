#!/usr/bin/env python3
"""
Web Dashboard for Support Ticket Agent Monitoring
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
import pandas as pd
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class DashboardData:
    def __init__(self):
        self.data_file = "dashboard_data.json"
        self.escalation_file = "escalation_log.csv"
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """Ensure data file exists"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({
                    "tickets_processed": 0,
                    "by_category": {"Billing": 0, "Technical": 0, "Security": 0, "General": 0},
                    "by_status": {"approved": 0, "rejected": 0, "escalated": 0},
                    "avg_processing_time": 0,
                    "success_rate": 100,
                    "recent_tickets": []
                }, f)
    
    def log_ticket(self, ticket_data, result):
        """Log a processed ticket"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Update statistics
            data["tickets_processed"] += 1
            data["by_category"][result.get("category", "Unknown")] += 1
            data["by_status"][result.get("review_status", "unknown")] += 1
            
            # Add to recent tickets
            recent_ticket = {
                "timestamp": datetime.now().isoformat(),
                "subject": ticket_data["subject"],
                "category": result.get("category", "Unknown"),
                "status": result.get("review_status", "unknown"),
                "retry_count": result.get("retry_count", 0),
                "response_length": len(result.get("draft_response", ""))
            }
            
            data["recent_tickets"].insert(0, recent_ticket)
            data["recent_tickets"] = data["recent_tickets"][:50]  # Keep last 50
            
            # Calculate success rate
            total = data["tickets_processed"]
            success = data["by_status"]["approved"]
            data["success_rate"] = round((success / total) * 100, 2) if total > 0 else 100
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error logging ticket: {e}")

# Global dashboard instance
dashboard_data = DashboardData()

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        with open(dashboard_data.data_file, 'r') as f:
            data = json.load(f)
        
        # Get escalation count
        escalation_count = 0
        if os.path.exists(dashboard_data.escalation_file):
            try:
                df = pd.read_csv(dashboard_data.escalation_file)
                escalation_count = len(df)
            except:
                escalation_count = 0
        
        return jsonify({
            "tickets_processed": data["tickets_processed"],
            "by_category": data["by_category"],
            "by_status": data["by_status"],
            "success_rate": data["success_rate"],
            "escalation_count": escalation_count,
            "recent_tickets": data["recent_tickets"][:10]  # Last 10 tickets
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tickets/recent')
def get_recent_tickets():
    """Get recent tickets"""
    try:
        with open(dashboard_data.data_file, 'r') as f:
            data = json.load(f)
        return jsonify(data["recent_tickets"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/escalations')
def get_escalations():
    """Get escalation data"""
    try:
        if os.path.exists(dashboard_data.escalation_file):
            df = pd.read_csv(dashboard_data.escalation_file)
            return jsonify(df.to_dict('records'))
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-ticket', methods=['POST'])
def api_process_ticket():
    """Process a ticket via API"""
    from src.agents.workflow import create_support_workflow
    from src.agents.state import State
    
    try:
        data = request.json
        ticket = {
            "subject": data.get('subject', ''),
            "description": data.get('description', '')
        }
        
        initial_state = State(
            ticket=ticket,
            category=None,
            context=None,
            draft_response=None,
            review_feedback=None,
            review_status=None,
            retry_count=0,
            messages=[]
        )
        
        workflow = create_support_workflow()
        result = workflow.invoke(initial_state)
        
        # Log to dashboard
        dashboard_data.log_ticket(ticket, result)
        
        return jsonify({
            "status": "success",
            "result": {
                "review_status": result.get('review_status'),
                "category": result.get('category'),
                "retry_count": result.get('retry_count', 0),
                "response": result.get('draft_response'),
                "context_items": len(result.get('context', []))
            }
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Support Ticket Agent Dashboard...")
    print("📍 http://localhost:5001")
    print("📊 Dashboard features:")
    print("   - Real-time statistics")
    print("   - Ticket processing analytics")
    print("   - Escalation management")
    print("   - API endpoint for ticket processing")
    app.run(debug=True, host='0.0.0.0', port=5001)