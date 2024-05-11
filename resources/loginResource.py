from flask_restful import Resource
from flask import request, jsonify
from flask import session
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn


def verify_password(email, password) -> bool:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    stored_password = cursor.fetchone()
    if stored_password is None:
        return False
    return stored_password[0] == password


class LoginPOSTResource(Resource):
    def get(self):
        return jsonify({"message": "Login successful!"})

    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if verify_password(email, password):
            session['logged_in'] = True

            access_token = create_access_token(identity=email)
            return jsonify({"success": True, "message": "Login successful!", "accessToken": access_token})
        else:
            return jsonify({"success": False, "message": "Invalid email or password", "accessToken": ""})

    @jwt_required()
    def delete(self):
        session.pop('logged_in', None)
        return jsonify({"message": "Logged out successfully!"})


class SignupPOSTResource(Resource):
    def post(self):
        user = request.get_json()
        conn = get_db_connection()
        conn.execute(
            f'INSERT INTO users (name, email, password, jobTitle, profileImage, aboutMe, experience) VALUES (?, ? ,? , ?, ?, ?, ?)',
            (user['name'], user['email'], user['password'], user["jobTitle"], user["profileImage"], user['aboutMe'],
             user['experience']))
        conn.commit()
        return jsonify({"success":True})


class LogoutGETResource(Resource):
    @jwt_required()
    def get(self):
        # Clear the session
        session.clear()
        return jsonify({"message": "Logged out successfully!"})
