import psycopg2 as pg
import csv

active_user = {
    "username": "Elek",
    "email": "a@b2.cd",
    "password": "HJkksdfjdvb4"
}


def user_registration(page, username, email, password):
    page.input_username().send_keys(username)
    page.input_email().send_keys(email)
    page.input_password().send_keys(password)
    page.submit_button().click()


def user_login(page, email=active_user["email"], password=active_user["password"]):
    page.input_email().clear()
    page.input_email().send_keys(email)
    page.input_password().clear()
    page.input_password().send_keys(password)
    page.submit_button().click()


def get_user(userflag):
    with open('test/users_data.csv', 'r', encoding='UTF-8') as datafile:
        users = list(csv.reader(datafile))
        for user in users:
            if user[5] == userflag:
                yield user


def database_query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == '__main__':
    get_user("invalid_user")
