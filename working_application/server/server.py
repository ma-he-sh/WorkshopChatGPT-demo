import uuid

from flask import Flask, Response, redirect, render_template, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from config import config
from modules.db.db import DB
from modules.db.sessions import SessionHandler
import json

import validators
import requests
import openai

from bs4 import BeautifulSoup
import re

from modules.model import ModelGPT

# initialize database
webdb = DB( config.DB_CONFIG )
webdb.db_create()
webdb.close()

app = Flask(__name__, static_url_path='/static', static_folder='build/static', template_folder='build')
CORS(app)

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

    return render_template('index.html', mapdata=maps, curr_session=uuid.uuid4())

@app.route('/valid_key', methods=['POST'])
def valid_key():
    payload = request.json

    api_key = payload['api_key']

    if api_key is None or len(api_key) == 0:
        resp = {
            'success': False,
            'response': 'API KEY required'
        }
        return send_response( False, resp )

    # validate if token is valid
    validToken = True
    openai.api_key = api_key
    try: 
        models = openai.Model.list()
    except:
        print('Error')
        validToken=False

    if not validToken:
        resp = {
            'success': False,
            'response': 'Invalid API-KEY'
        }
        return send_response( False, resp )

    resp = {
        'success': True,
        'response': 'Saved the API-KEY'
    }

    return send_response(True, resp)
    

@app.route('/get_infor', methods=['POST'])
def get_infor():
    payload = request.json
    
    api_key = payload['api_key']
    chat_site_content = payload['chat_site_content']
    prompt  = payload['prompt']

    if api_key is None or len(api_key) == 0:
        resp = {
            'success': False,
            'response': 'API KEY required'
        }
        return send_response( False, resp )

    if prompt is None or len(prompt) == 0:
        resp = {
            'success': False,
            'response': 'PROMPT required'
        }
        return send_response( False, resp )

    # validate if token is valid
    validToken = True
    openai.api_key = api_key
    try: 
        models = openai.Model.list()
    except:
        print('Error')
        validToken=False

    if not validToken:
        resp = {
            'success': False,
            'response': 'Invalid API-KEY'
        }
        return send_response( False, resp )

    model = ModelGPT( "", api_key )
    response = model.get_message( prompt, chat_site_content )

    resp = {
        'success': True,
        'prompt' : prompt,
        'response': response
    }

    return send_response(True, resp)

@app.route('/get_prompt', methods=['POST'])
def get_prompt():
    payload = request.json

    api_key = payload['api_key']
    site_url= payload['site_url']
    prompt  = payload['prompt']

    if api_key is None or len(api_key) == 0:
        resp = {
            'success': False,
            'response': 'API KEY required'
        }
        return send_response( False, resp )

    if site_url is None or len(site_url) == 0:
        resp = {
            'success': False,
            'response': 'SITE URL required'
        }
        return send_response( False, resp )

    if not validators.url( site_url ):
        resp = {
            'success': False,
            'response': 'SITE URL invalid'
        }
        return send_response( False, resp )

    if prompt is None or len(prompt) == 0:
        resp = {
            'success': False,
            'response': 'PROMPT required'
        }
        return send_response( False, resp )

    # validate if token is valid
    validToken = True
    openai.api_key = api_key
    try: 
        models = openai.Model.list()
    except:
        print('Error')
        validToken=False

    if not validToken:
        resp = {
            'success': False,
            'response': 'Invalid API-KEY'
        }
        return send_response( False, resp )
    
    page = requests.get(site_url)

    pageContent = ""
    if page:
        # parse the HTML document using BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser")

        # remove all script and style tags from the HTML document
        for script in soup(["script", "style", "a"]):
            script.decompose()

        # extract the text from the HTML document
        text = soup.get_text()

        # split the text into lines and then into chunks
        chunks = (phrase.strip() for line in text.splitlines() for phrase in line.split("  "))

        # join the non-empty chunks into a string
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text = ''.join(filter(lambda x: x.isprintable(), text))

        pageContent = text
    
    if not pageContent:
        resp = {
            'success': False,
            'response': 'Failed to request page content, please try another url'
        }
        return send_response( False, resp )

    model = ModelGPT( "", api_key )
    response = model.get_message( prompt, pageContent )

    resp = {
        'success': True,
        'prompt' : prompt,
        'response': response
    }

    return send_response(True, resp)

@app.errorhandler(404)
def error_404(e):
    return '404'

@app.errorhandler(500)
def error_500(e):
    return '500'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

