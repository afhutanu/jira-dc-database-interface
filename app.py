from flask import Flask, request, render_template_string, redirect, url_for, jsonify, session
import requests
import psycopg2
import json

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')
app.config['SECRET_KEY'] = '19250u12h0912b01bBGb0'

dbCreds = {}


from web.blueprints import ui, api
app.register_blueprint(ui.ui_blueprint)
app.register_blueprint(api.api_blueprint)


@app.before_request
def set_db_creds():
    if 'creds' in session:
        dbCreds.update(session['creds'])
        print("Updating creds from session")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)