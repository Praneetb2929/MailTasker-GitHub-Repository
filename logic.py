from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for flash messages

# Configure SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

POSTMARK_API_TOKEN = 'f263cf8c-d1cf-4acc-a451-ed9dd8a8340e'

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_address = db.Column(db.String(200))
    subject = db.Column(db.String(500))
    body = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')

with app.app_context():
    db.create_all()

def send_confirmation_email(to_address, subject, body):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': POSTMARK_API_TOKEN
    }
    payload = {
        "From": "2306351@kiit.ac.in",
        "To": to_address,
        "Subject": f"Task Received: {subject}",
        "TextBody": f"Hello,\n\nYour task has been added successfully.\n\nDetails:\nSubject: {subject}\nBody: {body}\n\nThanks!"
    }
    response = requests.post("https://api.postmarkapp.com/email", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"📧 Confirmation email sent to {to_address}")
    else:
        print(f"❌ Failed to send email: {response.status_code}, {response.text}")

@app.route('/inbound', methods=['POST'])
def inbound_email():
    data = request.get_json()
    task = Task(
        from_address=data.get('From'),
        subject=data.get('Subject'),
        body=data.get('TextBody'),
        status='Pending'
    )
    db.session.add(task)
    db.session.commit()
    print(f"✅ New task saved: {task.subject}")
    send_confirmation_email(task.from_address, task.subject, task.body)
    return jsonify({"message": "Task added to DB!"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = [{
        "id": t.id,
        "from": t.from_address,
        "subject": t.subject,
        "body": t.body,
        "status": t.status
    } for t in tasks]
    return jsonify(result)

@app.route('/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        task.status = 'Done'
        db.session.commit()
        return jsonify({"message": f"Task {task_id} marked as complete!"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<status>', methods=['GET'])
def get_tasks_by_status(status):
    tasks = Task.query.filter_by(status=status).all()
    result = [{
        "id": t.id,
        "from": t.from_address,
        "subject": t.subject,
        "body": t.body,
        "status": t.status
    } for t in tasks]
    return jsonify(result)

@app.route('/view-tasks')
def view_tasks():
    selected_status = request.args.get('status')
    if selected_status:
        tasks = Task.query.filter_by(status=selected_status).all()
    else:
        tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks, selected_status=selected_status)

@app.route('/mark-done/<int:task_id>')
def mark_done(task_id):
    task = db.session.get(Task, task_id)
    if task:
        task.status = 'Done'
        db.session.commit()
        flash(f"Task {task_id} marked as done.", "success")
    else:
        flash("Task not found.", "danger")
    return redirect(url_for('view_tasks'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash(f"Task {task_id} deleted.", "success")
    else:
        flash("Task not found.", "danger")
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
