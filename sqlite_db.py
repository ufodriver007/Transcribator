import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('transcribator.db')
    cur = base.cursor()
    base.execute('''
                    CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    user TEXT NOT NULL,
                    description TEXT NOT NULL,
                    file_id TEXT NOT NULL)''')
    base.commit()


async def sql_add(user, file_id, description):
    cur.execute('INSERT INTO data (user, file_id, description) VALUES (?, ?, ?)', (user, file_id, description))
    base.commit()

