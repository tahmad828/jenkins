from flask import Flask, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title') if data else None
        if title:
            task = Task(title=title)
            db.session.add(task)
            db.session.commit()
            return jsonify({"message": "Task added"}), 201
        return jsonify({"error": "Title required"}), 400

    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

