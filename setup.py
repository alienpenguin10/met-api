import sqlite3

def create_database():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        about_me TEXT,
        experience INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_name TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    connection.commit()
    connection.close()

def insert_dummy_data():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    # Insert dummy data into users table
    users = [
        (None, 'John Doe', 'john@example.com', 'password', 'About John', 5),
        (None, 'Jane Doe', 'jane@example.com', 'password', 'About Jane', 3),
    ]
    cursor.executemany('''
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
    ''', users)

    # Insert dummy data into events table
    events = [
        (None, 1, 'Event 1'),
        (None, 2, 'Event 2'),
    ]
    cursor.executemany('''
        INSERT INTO events VALUES (?, ?, ?)
    ''', events)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
    insert_dummy_data()
    