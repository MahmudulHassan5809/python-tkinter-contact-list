import sqlite3

class Database:
    DATABASE = "contacts.db"

    def __init__(self):
        self.conn = sqlite3.connect(Database.DATABASE)
        self.cur = self.conn.cursor()
        
    def create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name text, email text, phone_number text)")
        self.conn.commit()

    # def fetch(self, name=''):
    #     self.cur.execute(
    #         "SELECT * FROM contacts WHERE name LIKE ?", ('%'+name+'%',))
    #     rows = self.cur.fetchall()
    #     return rows

    def fetch(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insert(self, query, param):
        self.cur.execute(query,param)
        self.conn.commit()

    def remove(self, query, id):
        self.cur.execute(query, (id,))
        self.conn.commit()

    def update(self, query, param):
        self.cur.execute(query, param)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# db = Database()
# db.create_table()