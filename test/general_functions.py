import time
import psycopg2 as pg
import csv
import json


def user_registration(page, username, email, password):
    page.input_username().send_keys(username)
    page.input_email().send_keys(email)
    page.input_password().send_keys(password)
    page.submit_button().click()


def user_login(page, username, password):
    page.input_email().clear()
    page.input_email().send_keys(username)
    page.input_password().clear()
    page.input_password().send_keys(password)
    page.submit_button().click()


# get flag-based filtered user data
def get_users_from_file(userflag):
    with open('test/users_data.csv', 'r', encoding='UTF-8') as datafile:
        users = list(csv.reader(datafile))
        for user in users:
            if user[5] == userflag:
                yield user


# active user will be used through all tests
def set_active_user(username, email, password):
    user = {
        "username": username,
        "email": email,
        "password": password
    }
    with open("test/active_user.json", "w", encoding="UTF-8") as userdata:
        userdata.write((json.dumps(user)))


def get_active_user():
    with open("test/active_user.json", "r", encoding="UTF-8") as userdata:
        user = json.load(userdata)
        return user


def database_query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


def create_articles_from_file(page):
    article_titles = []
    with open("test/articles_data.csv", "r", encoding="UTF-8") as articles_file:
        articles = csv.reader(articles_file)
        next(articles)
        for article in articles:
            article_titles.append(article[0])
            page.new_article_link().click()
            page.article_title().send_keys(article[0])
            page.article_about().send_keys(article[1])
            page.article_body().send_keys(article[2])
            page.article_tags().send_keys(article[3])
            page.publish_button().click()
            page.signed_in_menu().click()
            page.my_articles().click()
    return article_titles


def modify_title(page):
    page.first_article_title().click()
    page.modify_article_link().click()
    page.article_title().click()
    reversed_title = page.article_title().get_attribute('value')[::-1]
    page.article_title().clear()
    page.article_title().send_keys(reversed_title)
    page.publish_button().click()
    page.signed_in_menu().click()
    return reversed_title


if __name__ == '__main__':
    # get_user("invalid_user")
    # update_active_user("bcc", "bcc", "ccc")
    get_active_user()
