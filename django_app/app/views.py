from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import json
import redis
import base64

redis_client = redis.Redis(host='localhost', port=6379, password='foobared', db=0)

def set_session_in_redis(session_key, data):
    encoded_data = base64.b64encode(json.dumps(data).encode()).decode()
    redis_client.set(session_key, encoded_data)

def get_session_from_redis(session_key):
    session_data = redis_client.get(session_key)
    if session_data:
        decoded_data = json.loads(base64.b64decode(session_data).decode())
        return decoded_data
    return {}

def delete_session_from_redis(session_key):
    redis_client.delete(session_key)

def login_view(request):
    session_id = request.COOKIES.get('session_id')
    if session_id:
        session_data = get_session_from_redis(session_id)
        if 'username' in session_data:
            return redirect('main')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            session_data = {'username': 'admin'}
            request.session['username'] = 'admin'
            # Django creates a new session here.
            if request.session.session_key is None:
                request.session.save()  # Force save to generate a session key.
            set_session_in_redis(request.session.session_key, session_data)
            response = redirect('main')
            response.set_cookie('session_id', request.session.session_key)
            return response
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def main_view(request):
    session_id = request.COOKIES.get('session_id')
    if session_id:
        session_data = get_session_from_redis(session_id)
        if 'username' in session_data:
            return render(request, 'main.html')
    return redirect('login')

def logout_view(request):
    session_id = request.COOKIES.get('session_id')
    if 'username' in request.session:
        del request.session['username']
        delete_session_from_redis(session_id)
    response = redirect('login')
    response.delete_cookie('session_id')
    return response