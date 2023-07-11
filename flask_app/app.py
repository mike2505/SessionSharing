from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
import redis
import json
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, password='foobared', db=0)
app.config['SESSION_COOKIE_NAME'] = 'flask-shared-session'
app.config['SESSION_COOKIE_SAMESITE'] = None
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)

def set_session_in_redis(session_key, data):
    encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
    app.session_interface.redis.set(session_key, encoded_data)

def get_session_from_redis(session_key):
    session_data = app.session_interface.redis.get(session_key)
    if session_data:
        decoded_data = json.loads(base64.b64decode(session_data).decode())
        return decoded_data
    return {}

def delete_session_from_redis(session_key):
    app.session_interface.redis.delete(session_key)

@app.route('/', methods=['GET', 'POST'])
def login():
    session_id = request.cookies.get('session_id')
    if session_id:
        session_data = get_session_from_redis(session_id)
        if 'username' in session_data:
            return redirect(url_for('main'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session_data = {'username': 'admin'}
            session['username'] = 'admin'
            if session.sid is None:
                session.modified = True  # Force the session to be stored.
            set_session_in_redis(session.sid, session_data)
            response = redirect(url_for('main'))
            response.set_cookie('session_id', session.sid)
            return response

    session_id = request.cookies.get('session_id')
    if session_id:
        session_data = get_session_from_redis(session_id)
        if 'username' in session_data:
            return redirect(url_for('main'))

    return render_template('login.html')

@app.route('/main')
def main():
    session_id = request.cookies.get('session_id')
    if session_id:
        session_data = get_session_from_redis(session_id)
        if 'username' in session_data:
            return render_template('main.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        session.pop('username', None)
        delete_session_from_redis(session_id)
    response = redirect(url_for('login'))
    response.delete_cookie('session_id')
    return response

if __name__ == "__main__":
    app.run(debug=True)
