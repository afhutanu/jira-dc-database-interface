import json
from flask import Blueprint, redirect, render_template, request, url_for, session
import requests
from web.repositories import *
from requests.auth import HTTPBasicAuth

ui_blueprint = Blueprint('ui', __name__) 


@ui_blueprint.route('/')
def home():
    return render_template("home.html")
    

@ui_blueprint.route('/options', methods=['POST'])
def options():
    auth_type = request.form['auth_type']
    url = "https://instance-name/rest/scriptrunner/latest/custom/dbAuth"
    
    if auth_type == 'basic':
        username = request.form['username']
        password = request.form['password']

        response = requests.get(url, auth=HTTPBasicAuth(username, password))
    elif auth_type == 'bearer':
        token = request.form['token']
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
    else:
        return "Invalid authentication type."

    if response.status_code == 200:
        credentials = response.json()['credentials']
        session['creds'] = credentials  # Store the credentials in the session

        return render_template("options.html")
    else:
        return f"Failed to fetch data: {response.status_code}"
    

    