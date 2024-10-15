from calendar import c
import sqlite3

def create_db_table():
    conn = sqlite3.connect('scores.sql')
    c = conn.cursor()
    c.execute("CREATE TABLE scores (nick TEXT, score INTEGER)")
    c.execute("INSERT INTO scores VALUES ('GOD', 1000)")
    c.execute("INSERT INTO scores VALUES ('Sarah', 717)")
    c.execute("INSERT INTO scores VALUES ('john', 92)")
    conn.commit()
    conn.close()

def insert_new_score(nick, score):
    conn = sqlite3.connect('scores.sql')
    c = conn.cursor()
    c.execute("INSERT INTO scores VALUES (?, ?)", (nick, score))
    conn.commit()
    conn.close()

def show_high_scores():
    conn = sqlite3.connect('scores.sql')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY scores.score DESC LIMIT 5')
    best_scores = c.fetchall()
    conn.close()

    return best_scores

def delete_db_table():
    conn = sqlite3.connect('scores.sql')
    c = conn.cursor()
    c.execute('DROP TABLE scores')
    conn.commit()
    conn.close()
