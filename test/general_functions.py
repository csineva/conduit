import psycopg2 as pg
import csv
import json


# fills up the registration input fields, then submit
def user_registration(page, username, email, password):
    page.input_username().send_keys(username)
    page.input_email().send_keys(email)
    page.input_password().send_keys(password)
    page.submit_button().click()


# fills up the login input fields, then submit
def user_login(page, email, password):
    page.input_email().clear()
    page.input_email().send_keys(email)
    page.input_password().clear()
    page.input_password().send_keys(password)
    page.submit_button().click()


# get flag-based filtered user data from file
def get_users_from_file(userflag):
    with open('test/users_data.csv', 'r', encoding='UTF-8') as datafile:
        users = list(csv.reader(datafile))
        for user in users:
            if user[5] == userflag:
                yield user


# save valid user data to file, active user will be used through all tests
def set_active_user(username, email, password):
    user = {
        "username": username,
        "email": email,
        "password": password
    }
    with open("test/active_user.json", "w", encoding="UTF-8") as userdata:
        userdata.write((json.dumps(user)))


# returns with active user data from file
def get_active_user():
    with open("test/active_user.json", "r", encoding="UTF-8") as userdata:
        user = json.load(userdata)
        return user


# returns with sql query results from postgres database
def database_query(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# saves the article previews to file
def save_articles_to_file(articles, abouts):
    articles_length = len(articles)
    with open("test/article_preview_from_mainpage.csv", "w", encoding="UTF-8") as article_file:
        article_file.write("article title,article about\n")
        for index in range(articles_length):
            article_file.write(f'{articles[index].text},{abouts[index].text}\n')


# load the article previews from file
def load_articles_from_file():
    with open("test/article_preview_from_mainpage.csv", "r", encoding="UTF-8") as article_file:
        next(article_file)
        articles = list(csv.reader(article_file))
        for article in articles:
            yield article


# load some article test data from file and create articles
def create_articles_from_file(page):
    article_titles = []
    with open("test/articles_data.csv", "r", encoding="UTF-8") as articles_file:
        articles = csv.reader(articles_file)
        next(articles)
        for article in articles:
            article_titles.append(article[0])
            page.create_article_link().click()
            page.input_article_title().send_keys(article[0])
            page.input_article_about().send_keys(article[1])
            page.input_article_body().send_keys(article[2])
            page.input_article_tags().send_keys(article[3])
            page.publish_button().click()
            page.signed_in_menu().click()
            page.my_articles().click()
    return article_titles


# modifies the first article
def modify_title(page):
    page.first_article_title().click()
    page.modify_article_link().click()
    page.input_article_title().click()
    reversed_title = page.input_article_title().get_attribute('value')[::-1]
    page.input_article_title().clear()
    page.input_article_title().send_keys(reversed_title)
    page.publish_button().click()
    page.signed_in_menu().click()
    return reversed_title


# delete all test articles created before
def delete_articles(page):
    articles = len(page.articles_titles())
    for index in range(articles):
        page.my_articles().click()
        page.first_article_title().click()
        page.delete_article_button().click()
        page.refresh()
        page.signed_in_menu().click()
        page.my_articles().click()
    page.refresh()


if __name__ == '__main__':
    # get_user("invalid_user")
    # update_active_user("bcc", "bcc", "ccc")
    get_active_user()
