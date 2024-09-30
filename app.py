# app.py
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = []
notes = []

@app.route('/')
def index():
    if 'username' in session:
        user_notes = [note for note in notes if note['username'] == session['username']]
        return render_template('notes.html', notes=user_notes)
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if any(user['username'] == username for user in users):
        return 'User already exists'
    users.append({'username': username, 'password': password})
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user:
        session['username'] = username
        return redirect(url_for('index'))
    return 'Invalid credentials'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'username' in session:
        title = request.form['title']
        content = request.form['content']
        notes.append({'username': session['username'], 'title': title, 'content': content})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
