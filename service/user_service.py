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

    def login(self, username,password):
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE username='{username}' AND password='{password}'")
        user = cur.fetchall()
        con.close()
        return user

    def delete(self, user_request):
        username = user_request['username']
        password = user_request['password']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"DELETE FROM users WHERE username='{username}' AND password='{password}'")
        con.close()

    def change_password(self, user_request):
        username = user_request['username']
        newPassword = user_request['newPassword']
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"UPDATE users SET password='{newPassword}' WHERE username='{username}'")
        con.close()
