from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize app and configure SQLite DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_address = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')

# Initialize DB tables
with app.app_context():
    db.create_all()

# Inbound email route
@app.route('/inbound', methods=['POST'])
def inbound_email():
    data = request.get_json()

    simplified_data = {
        'From': data.get('From'),
        'Subject': data.get('Subject'),
        'TextBody': data.get('TextBody')
    }

    print(f"Received email data:\n{simplified_data}")

    new_task = Task(
        from_address=simplified_data['From'],
        subject=simplified_data['Subject'],
        body=simplified_data['TextBody'],
        status='Pending'
    )
    db.session.add(new_task)
    db.session.commit()

    print(f"✅ New task saved: {simplified_data['Subject']}")

    return "OK", 200

# Get all tasks route
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        "id": task.id,
        "from": task.from_address,
        "subject": task.subject,
        "body": task.body,
        "status": task.status
    } for task in tasks]

    return jsonify(task_list)

# Mark a task as complete
@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found."}), 404

    task.status = "Complete"
    db.session.commit()

    return jsonify({"message": f"Task {task_id} marked as complete!"}), 200

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
