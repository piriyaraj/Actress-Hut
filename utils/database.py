import os
import sqlite3

class Database:
    def __init__(self):
        self.db_file_path = os.path.abspath("src/database/playlist.sqlite3")
        self.conn = sqlite3.connect(self.db_file_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE
            )
        ''')

    def getPlayListId(self, playListName):
        '''get the id of the playlist from the .db file database
        return id, status (True/False)
        '''
        try:
            self.cursor.execute('SELECT id FROM playlists WHERE name = ?', (playListName,))
            row = self.cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
        except sqlite3.Error as e:
            print(e)
            return None

    def setPlayListId(self, id, playListName):
        '''add the playlist id and name in the .db file database'''
        try:
            self.cursor.execute('INSERT INTO playlists (id, name) VALUES (?, ?)', (id, playListName,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
