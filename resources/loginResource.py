from flask_restful import Resource
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask import Flask, session
from flask_session import Session
import sqlite3


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password) -> bool:
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    stored_password = cursor.fetchone()
    if stored_password is None:
        return False
    return stored_password[0] == password

class LoginPOSTResource(Resource):
    @auth.login_required
    def get(self):
        return jsonify({"message": "Login successful!"})
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if verify_password(email, password):
            session['logged_in'] = True
            return jsonify({"success": True,"message": "Login successful!"})
        else:
            print(jsonify({"success": "false","message": "Invalid email or password"}))
            return jsonify({"success": False,"message": "Invalid email or password"})
    
    @auth.login_required
    def delete(self):
        session.pop('logged_in', None)
        return jsonify({"message": "Logged out successfully!"})
    
class LogoutGETResource(Resource):
    @auth.login_required
    def get(self):
        # Clear the session
        session.clear()
        return jsonify({"message": "Logged out successfully!"})