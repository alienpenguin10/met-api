from flask_restful import Resource
from flask import request
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn


class UserEventsGETResource(Resource):
    def get(self, id):
        conn = get_db_connection()
        events = conn.execute('SELECT events.id,events.name, events.date FROM events INNER JOIN user_events ON events.id = user_events.eventId WHERE user_events.userId = ?', (id,)).fetchall()
        conn.close()
        return [dict(event) for event in (events if events else [])]

class UserEventsPOSTResource(Resource):
    def post(self,id):
        json = request.get_json()
        conn = get_db_connection()
        conn.execute(f'INSERT INTO user_events (userId, eventId) VALUES (?, ?)', (id,json['event']))
        conn.commit()
        conn.close()
        return {'success':True}

class UserEventsDELETEResource(Resource):
    def delete(self, id):
        json = request.get_json()
        conn = get_db_connection()
        conn.execute('DELETE FROM users_events WHERE userId = ? AND eventId = ?', (id,json['event'],))
        conn.commit()
        conn.close()
        return {'success':True}
    
