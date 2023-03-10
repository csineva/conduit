import psycopg2 as pg


def query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# user tábla összes adatának lekérdezése
print(query('SELECT * FROM users'))

# user2-re végződő nevű user(ek) lekérdezése
print(query("SELECT * FROM users WHERE username LIKE '%user2'"))
print()

# testuser2 felhasználó nevének és e-mail címének lekérdezése, változókba mentése
username, email = query("SELECT username, email FROM users WHERE username = 'testuser2'")[0]
print(f'A felhasználó neve: {username}\nA felhasználo e-mail címe: {email}')