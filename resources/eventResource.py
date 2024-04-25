from flask_restful import Resource
from flask import request
import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

class EventsGETResource(Resource):
    def get(self):
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM events').fetchall()
        conn.close()
        return [dict(event) for event in events]

class EventGETResource(Resource):
    def get(self, id):
        conn = get_db_connection()
        event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
        conn.close()
        return dict(event) if event else None

class EventPOSTResource(Resource):
    def post(self):
        event = request.get_json()
        conn = get_db_connection()
        conn.execute('INSERT INTO events (user_id, event_name) VALUES (?, ?)', (event['user_id'], event['event_name']))
        conn.commit()
        new_event_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return {'id': new_event_id, **event}

class EventPUTResource(Resource):
    def put(self, id):
        event = request.get_json()
        conn = get_db_connection()
        conn.execute('UPDATE events SET user_id = ?, event_name = ? WHERE id = ?', (event['user_id'], event['event_name'], id))
        conn.commit()
        conn.close()
        return {'id': id, **event}

class EventDELETEResource(Resource):
    def delete(self, id):
        conn = get_db_connection()
        conn.execute('DELETE FROM events WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return "", 204