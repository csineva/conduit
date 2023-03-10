import bcrypt
import psycopg2 as pg


def query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# get the pass from postgres db
pass_from_db = query("SELECT password FROM users WHERE username = 'alma'")[0][0]
print(pass_from_db)
encoded_hash = pass_from_db.encode('utf-8')  #encoding needed to array of bytes

# local password to compare with
passwd = 'Almaalma1'
print(passwd)
encoded_passwd = passwd.encode('utf-8')  #encoding needed to array of bytes

# no red stuff if True:
assert bcrypt.checkpw(encoded_passwd, encoded_hash)
