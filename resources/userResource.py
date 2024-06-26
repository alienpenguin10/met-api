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
    def get(self, id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        conn.close()
        return dict(user) if user else None

class UserPOSTResource(Resource):
    def post(self):
        user = request.get_json()
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email, password, about_me, experience) VALUES (?, ?)', (user['name'], user['email'], user['password'], user['about_me'], user['experience']))
        conn.commit()
        new_user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return {'id': new_user_id, **user}

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