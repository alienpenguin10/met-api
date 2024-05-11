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
        jobTitle TEXT,
        profileImage TEXT,
        aboutMe TEXT,
        experience INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER,
        eventId INTEGER,
        FOREIGN KEY(userId) REFERENCES users(id),
        FOREIGN KEY(eventId) REFERENCES events(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1Id INTEGER,
        user2Id INTEGER,
        conversations REAL,
        conversationLength REAL,
        confirmed INTEGER,
        firstMet INTEGER,
        FOREIGN KEY(user1Id) REFERENCES users(id),
        FOREIGN KEY(user2Id) REFERENCES users(id),
        FOREIGN KEY (firstMet) REFERENCES events(id)
    )
    ''')

    connection.commit()
    connection.close()


def insert_dummy_data():
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    # Insert dummy data into users table
    users = [
        (None, 'Seiko', 'sy946@bath.ac.uk', 'password', 'CEO Of MET', 'profileImage', 'About Seiko', 1),
        (None, 'Sam', 'sl3168@bath.ac.uk', 'password', 'CTO', 'profileImage', 'About Sam', 1),
        (None, 'Jonah', 'jk2258@bath.ac.uk', 'password', 'Software Engineer', 'profileImage', 'About Jonah', 1),
        (None, 'Varnie', 'vk545@bath.ac.uk', 'password', 'Software Engineer', 'profileImage', 'About Varnie', 1),
        (None, 'Han', 'ch2730@bath.ac.uk', 'password', 'Software Engineer', 'profileImage', 'About Han', 1)
    ]
    cursor.executemany('''
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)

    # Insert dummy data into events table
    events = [
        (None, 'RebelMeetups', '2024-04-23'),
        (None, 'Bath Digital Festival', '2024-05-14'),
        (None, 'Future of AI', '2025-09-01'),
    ]
    cursor.executemany('''
        INSERT INTO events VALUES (?, ?, ?)
    ''', events)

    # Insert dummy data into user_events table
    events_assignment = [
        (None, 1, 2),
        (None, 1, 3),

        (None, 2, 2),
        (None, 2, 3),

        (None, 3, 2),
        (None, 3, 3),

        (None, 4, 2),
        (None, 4, 3),

        (None, 5, 2),
        (None, 5, 3),
    ]
    cursor.executemany('''
        INSERT INTO user_events VALUES (?, ?, ?)
    ''', events_assignment)

    # Insert dummy data into connections table
    connections = [
        (None, 1, 2, 10.0, 15.0, int(True), 1),
        (None, 1, 5, 5.0, 20.0, int(False), 1),
        (None, 1, 4, 8.0, 10.0, int(True), 1),

        (None, 2, 3, 5.0, 20.0, int(False), 1),
        (None, 2, 4, 8.0, 12.0, int(False), 1),

        (None, 3, 1, 3.0, 30.0, int(False), 1),
        (None, 3, 4, 6.0, 10.0, int(True), 1),

        (None, 4, 5, 2.0, 4.0, int(True), 1),

        (None, 5, 2, 12.0, 15.0, int(True), 1),
        (None, 5, 3, 40.0, 60.0, int(False), 1),
    ]
    cursor.executemany('''
        INSERT INTO connections VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', connections)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    insert_dummy_data()
