from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

class EventsGETResource(Resource):
    @jwt_required()
    def get(self):
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM events').fetchall()
        conn.close()
        return [dict(event) for event in events]

class EventGETResource(Resource):
    @jwt_required()
    def get(self, id):
        conn = get_db_connection()
        event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
        conn.close()
        return dict(event) if event else None

class EventPOSTResource(Resource):
    @jwt_required()
    def post(self):
        event = request.get_json()
        conn = get_db_connection()
        conn.execute('INSERT INTO events (name) VALUES (?, ?)', (event['name'],event['date']))
        conn.commit()
        new_eventId = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return {'id': new_eventId, **event}

class EventPUTResource(Resource):
    @jwt_required()
    def put(self, id):
        event = request.get_json()
        conn = get_db_connection()
        conn.execute('UPDATE events SET userId = ?, name = ? WHERE id = ?', (event['name'],event['date'], id))
        conn.commit()
        conn.close()
        return {'id': id, **event}

class EventDELETEResource(Resource):
    @jwt_required()
    def delete(self, id):
        conn = get_db_connection()
        conn.execute('DELETE FROM events WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return "", 204