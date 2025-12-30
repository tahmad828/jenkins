from flask import Flask, render_template, request, redirect, url_for
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
        title = request.form.get('title')
        if title:
            task = Task(title=title)
            db.session.add(task)
            db.session.commit()
        return redirect(url_for('index'))

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
