from flask_restful import Resource
from flask import request
import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

class UsersGETResource(Resource):
    def get(self):
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(user) for user in users]

class UserGETResource(Resource):
    def get(self, email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

class UserPOSTResource(Resource):
    def post(self):
        user = request.get_json()
        conn = get_db_connection()
        new_user_id = conn.execute(f"SELECT MAX(id) FROM users").fetchone()[0] + 1
        print(new_user_id)
        conn.execute(f'INSERT INTO users (id, name, email, password, jobTitle, profileImage, aboutMe, experience) VALUES (?, ?, ? ,? , ?, ?, ?, ?)', (new_user_id, user['name'], user['email'], user['password'], user["jobTitle"], user["profileImage"], user['aboutMe'], user['experience']))
        conn.commit()
        
        conn.close()
        return {'success':True}

class UserPUTResource(Resource):
    def put(self, id):
        user = request.get_json()
        conn = get_db_connection()
        conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (user['name'], user['email'], id))
        conn.commit()
        conn.close()
        return {'id': id, **user}

class UserDELETEResource(Resource):
    def delete(self, id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return "", 204