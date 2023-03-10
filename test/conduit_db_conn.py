import psycopg2 as pg

def query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

print(query('SELECT * FROM users'))
print(query("SELECT username, email FROM users WHERE username LIKE '%user2'"))
print()
username, email = query("SELECT username, email FROM users WHERE username = 'testuser2'")[0]
print(f'A felhasználó neve: {username}\nA felhasználo e-mail címe: {email}')