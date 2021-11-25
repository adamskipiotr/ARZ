import sqlite3

DATABASE = 'database.db'


class UserService:

    def save(self, user_request):
        username = user_request['username']
        password = user_request['password']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"INSERT INTO users (username, password) VALUES('{username}','{password}')")
        con.commit()
        con.close()

    def login(self, login_request):
        username = login_request['username']
        password = login_request['password']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE username='{username}' AND password='{password}'")
        user = cur.fetchall()
        con.close()
        return user
