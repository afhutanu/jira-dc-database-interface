import json
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, session
import requests
from web.repositories import *
from requests.auth import HTTPBasicAuth


api_blueprint = Blueprint('api', __name__, url_prefix='/api') 


@api_blueprint.route('/search_user', methods=['GET'])
def search_user():
    print("Searching for user")
    search_term = request.args.get('searchTerm')
    creds = session.get('creds')[0]  # Assuming first set of credentials
    conn = get_db_connection(creds['username'], creds['password'])
    if conn:
        cur = conn.cursor()
        try:
            like_pattern = f'%{search_term}%'
            cur.execute("SELECT rolname FROM pg_roles WHERE rolname LIKE %s", (like_pattern,))
            roles = cur.fetchall()
            results_html = '<ul class="list-group">'
            if roles:
                for role in roles:
                    results_html += f'<li class="list-group-item">{role[0]}</li>'
            else:
                results_html += '<li class="list-group-item">No results found</li>'
            results_html += '</ul>'
            return results_html
        except Exception as e:
            print(f"Error in database query: {str(e)}")
            return "Error in database query"
        finally:
            cur.close()
            conn.close()
    else:
        return "Failed to connect to database"


@api_blueprint.route('/create_schema', methods=['POST'])
def create_schema():
    print(f"Received POST data: {request.form}")
    try:
        schema_name = request.form.get('schemaName')
        creds = session.get('creds')

        if not creds or not schema_name:
            print("Error: Missing credentials or schema name")
            return jsonify({'error': 'Missing credentials or schema name'}), 400

        print(f"Creds are: {creds}")
        creds = creds[0]  # Assuming first set of credentials
        print(f"Using credentials: {creds}")
        conn = get_db_connection(creds['username'], creds['password'])

        if not conn:
            print("Error: Failed to connect to database")
            return jsonify({'error': 'Failed to connect to database'}), 500

        cur = conn.cursor()
        try:
            cur.execute(f"CREATE SCHEMA {schema_name}")
            cur.execute(f"SELECT add_views_to_schema('{schema_name}')")
            result = cur.fetchone()  # If function returns something
            if result:
                print(f"Result from adding user to schema: {result}")
            conn.commit()
            print(f"Schema created and views added successfully: {schema_name}")
            return jsonify({'message': f'Schema {schema_name} created successfully and views added.'})
        except Exception as e:
            print(f"Failed to add user to schema: {str(e)}")
            return jsonify({'message': str(e)}), 500


    except Exception as e:
        print(f"Failed to create schema: {str(e)}")
        return jsonify({'message': str(e)}), 500


@api_blueprint.route('/create_user', methods=['POST'])
def create_user():
    print(f"Received POST data for user creation: {request.form}")
    user_name = request.form['userName']
    schema_name = request.form['schemaName']
    password = request.form['password']
    creds = session.get('creds')

    if not creds:
        print("Error: Credentials are missing")
        return jsonify({'error': 'Credentials are missing'}), 400

    creds = creds[1]  # Assuming second set of credentials
    print(f"Using credentials: {creds}")
    conn = get_db_connection(creds['username'], creds['password'])

    if not conn:
        print("Error: Failed to connect to database")
        return jsonify({'error': 'Failed to connect to database'}), 500

    cur = conn.cursor()
    try:
        cur.execute(f"CREATE ROLE {user_name} LOGIN PASSWORD %s", (password,))
        print(f"Role {user_name} created with login.")
        cur.execute(f"GRANT CONNECT ON DATABASE instance-nameprod TO {user_name}")
        cur.execute(f"ALTER USER {user_name} SET search_path TO {schema_name}, public")
        conn.commit()
        print(f"User {user_name} created successfully and permissions set.")
        return jsonify({'message': f'User {user_name} created successfully and permissions set.'})
    except Exception as e:
        print(f"Failed to create user: {str(e)}")
        return jsonify({'message': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@api_blueprint.route('/add_user_to_schema', methods=['POST'])
def add_user_to_schema():
    print(f"Received POST data for adding user to schema: {request.form}")
    schema_name = request.form['schemaName']
    user_name = request.form['userName']
    creds = session.get('creds')

    if not creds:
        print("Error: Credentials are missing")
        return jsonify({'error': 'Credentials are missing'}), 400

    creds = creds[0]  # Assuming first set of credentials again
    print(f"Using credentials: {creds}")
    conn = get_db_connection(creds['username'], creds['password'])

    if not conn:
        print("Error: Failed to connect to database")
        return jsonify({'error': 'Failed to connect to database'}), 500

    cur = conn.cursor()
    try:
        cur.execute(f"SELECT add_views_to_schema('{schema_name}')")
        cur.execute(f"SELECT add_user_to_schema('{schema_name}', '{user_name}')")
        result = cur.fetchone()  # If function returns something
        if result:
            print(f"Result from adding user to schema: {result}")
        conn.commit()
        print(f"User {user_name} added to schema {schema_name} successfully.")
        return jsonify({'message': f'User {user_name} added to schema {schema_name} successfully.'})
    except Exception as e:
        print(f"Failed to add user to schema: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
