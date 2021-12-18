import sqlite3


DATABASE = 'database.db'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS animals_recognition (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, attempts INTEGER, positive INTEGER)")

animals = ["chicken", "elephant", "cat"]
c.execute(f"SELECT id FROM animals_recognition")
fetched_animals = c.fetchall()
if len(fetched_animals) == 0:
    for animal in animals:
        name = animal
        attempts = 0
        positive = 0
        values = (name,attempts, positive)
        c.execute("INSERT OR IGNORE INTO animals_recognition VALUES(null,?,?,?)", values)
        conn.commit()
conn.close()
