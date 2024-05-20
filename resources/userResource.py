from flask_restful import Resource
from flask import request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn


class UsersGETResource(Resource):
    @jwt_required()
    def get(self):
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(user) for user in users]


class UserGETResource(Resource):
    @jwt_required()
    def get(self, id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        conn.close()
        return dict(user) if user else None


class UserFromEmailGetResource(Resource):
    @jwt_required()
    def get(self, email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None


class UserPOSTResource(Resource):
    @jwt_required()
    def post(self):
        user = request.get_json()
        conn = get_db_connection()
        conn.execute(
            f'INSERT INTO users (name, email, password, jobTitle, profileImage, aboutMe, experience) VALUES (?, ? ,? , ?, ?, ?, ?)',
            (user['name'], user['email'], user['password'], user["jobTitle"], user["profileImage"], user['aboutMe'],
             user['experience']))
        conn.commit()

        conn.close()
        return {'success': True}


class UserPUTResource(Resource):
    @jwt_required()
    def put(self, id):
        user = request.get_json()
        conn = get_db_connection()
        conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (user['name'], user['email'], id))
        conn.commit()
        conn.close()
        return {'id': id, **user}


class UserDELETEResource(Resource):
    @jwt_required()
    def delete(self, id):
        if id != get_jwt_identity():
            return jsonify({"Success":False})

        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.execute('DELETE FROM user_events WHERE userId = ?',(id,))
        conn.execute('DELETE FROM connections WHERE user1Id = ? OR user2Id = ?', (id,id))
        conn.commit()
        conn.close()
        return jsonify({"Success":True})
