from flask_restful import Resource
from flask import request
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

class ConnectionsGETResource(Resource):
    def get(self,id):
        conn = get_db_connection()
        connections = conn.execute('SELECT * FROM connections WHERE user1Id = ? OR user2Id = ?',(id,id)).fetchall()
        result = []
        for connection in connections:
            dictConnection = dict(connection)
            if dictConnection['user1Id'] == id:
                otherId = dictConnection['user2Id']
            else:
                otherId = dictConnection['user1Id']
            dictConnection['user'] = dict(conn.execute('SELECT * FROM users WHERE id = ?', (otherId,)).fetchone())
            dictConnection.pop('user1Id')
            dictConnection.pop('user2Id')
            result.append(dictConnection)
        conn.close()
        return result

class ConnectionsPOSTResource(Resource):
    def post(self):
        connections = request.get_json()
        conn = get_db_connection()
        conn.execute('INSERT INTO connections (user1Id,user2Id,conservations,conservationLength) VALUES (?, ?, ?, ?)', (connections['user1Id'],connections['user2Id'],connections['conservations'],connections['conservationLength']))
        conn.commit()
        conn.close()
        return {'success':True}

class ConnectionsPUTResource(Resource):
    def put(self):
        connections = request.get_json()
        conn = get_db_connection()
        conn.execute('UPDATE connections SET conservationLength = ? WHERE user1Id = ? AND user2Id = ?', (connections['conservationLength'],connections['user1Id'],connections['user2Id']))
        conn.commit()
        conn.close()
        return {'success':True}

class ConnectionsDELETEResource(Resource):
    def delete(self):
        conn = get_db_connection()
        connections = request.get_json()
        conn.execute('DELETE FROM connections WHERE user1Id = ? AND user2Id = ?', (connections['user1Id'],connections['user2Id']))
        conn.commit()
        conn.close()
        return {'success':True}
        