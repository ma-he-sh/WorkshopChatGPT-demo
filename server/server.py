import uuid

from flask import Flask, Response, redirect, render_template, request, jsonify
from flask_bcrypt import Bcrypt
from config import config
from modules.db.db import DB
from modules.db.sessions import SessionHandler
import json

from flask_socketio import SocketIO, join_room, leave_room, send, emit

# initialize database
webdb = DB( config.DB_CONFIG )
webdb.db_create()
webdb.close()

app = Flask(__name__, static_url_path='/static', static_folder='build/static', template_folder='build')
socket = SocketIO(app)

def send_response(is_success=False, payload=None):
    if payload is None:
        payload = {}
    return jsonify(
        success=is_success,
        payload=payload
    )

@app.route('/', methods=['GET'])
def root():
    sessionHandler = SessionHandler(config.DB_CONFIG)
    maps = sessionHandler.get_all()
    
    return render_template('index.html', mapdata=maps)

@app.errorhandler(404)
def error_404(e):
    return '404'

@app.errorhandler(500)
def error_500(e):
    return '500'

if __name__ == '__main__':
    socket.run(app, debug=True, host='0.0.0.0', port=8000)

