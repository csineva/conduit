# *** Regisztráció ***
# Bejelentkezés
# Adatkezelési nyilatkozat használata
# Adatok listázása
# Több oldalas lista bejárása
# Új adat bevitel
# Ismételt és sorozatos adatbevitel adatforrásból
# Meglévő adat módosítás
# Adat vagy adatok törlése
# Adatok lementése felületről
# Kijelentkezés

import psycopg2 as pg

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--lang=en")
browser = webdriver.Chrome(service=service, options=options)
# browser.implicitly_wait(10)

URL = "http://localhost:1667/#/"
browser.get(URL)


# user registration function, returns with registration response text
def sign_up(user, email, password):
    find = browser.find_element

    register = find(By.LINK_TEXT, "Sign up")
    register.click()

    signup_page_check = find(By.TAG_NAME, "h1").text  #let's check if we are on the right spot
    assert signup_page_check == 'Sign up'

    input_username = find(By.XPATH, '//input[@placeholder="Username"]')  # let's dance!
    input_email = find(By.XPATH, '//input[@placeholder="Email"]')
    input_password = find(By.XPATH, '//input[@placeholder="Password"]')
    submit_btn = find(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    input_username.send_keys(user)
    input_email.send_keys(email)
    input_password.send_keys(password)
    submit_btn.click()

    reg_result = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]'))).text
    reg_info = find(By.XPATH, '//div[@class="swal-text"]').text
    confirm_btn = find(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
    confirm_btn.click()

    return f'{reg_result} {reg_info}'


# database query function, returns with sql result
def query_db(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


# 'valid_...' keys as expected result
test_data = [
    {
        'user': '',  #empty username
        'email': 'cs@g.gg',
        'valid_email': True,
        'password': 'Almafafa1',
        'valid_password': True
    },
    {
        'user': 'alma',
        'email': '',  # empty email
        'valid_email': False,
        'password': 'GHkjheeb453',
        'valid_password': True
    },
    {
        'user': 'körte',
        'email': 'cs@g.gl',
        'valid_email': True,
        'password': '',  # empty password
        'valid_password': False
    },
    {
        'user': 'alma',
        'email': 'cs@g.g',  # invalid email
        'valid_email': False,
        'password': 'GHkjheeb453',
        'valid_password': True
    },
    {
        'user': 'alma',
        'email': 'cs@g.gl',  # email valid, but exists in db
        'valid_email': True,
        'password': 'HDirfkvid432',
        'valid_password': True
    },
    {
        'user': 'alma',
        'email': 'a@b.cd',
        'valid_email': True,
        'password': 'zokni',  # invalid password
        'valid_password': False
    },
    {
        'user': 'alma',
        'email': 'cs@g.ga',
        'valid_email': True,
        'password': 'JHHkjshdk12',
        'valid_password': True
    }
]

responses = {
    'empty_username': 'Registration failed! Username field required.',
    'empty_email': 'Registration failed! Email field required.',
    'invalid_email': 'Registration failed! Email must be a valid email.',
    'empty_password': 'Registration failed! Password field required.',
    'invalid_password': 'Registration failed! Password must be 8 characters long '
                        'and include 1 number, 1 uppercase letter, and 1 lowercase letter.',
    'email_taken': 'Registration failed! Email already taken.',
    'success': 'Welcome! Your registration was successful!',
}

for data in test_data:
    email_exists = query_db(f"SELECT email FROM users WHERE email = '{data['email']}'")  # check database if email exists already
    signup_result = sign_up(data['user'], data['email'], data['password'])

    print(f"user: {data['user']}, mail: {data['email']}, pass: {data['password']}")
    print(signup_result)
    print()

    # responses check if fits expected results
    if not data['user']:
        assert signup_result == responses['empty_username']
    elif not data['email']:
        assert signup_result == responses['empty_email']
    elif not data['password']:
        assert signup_result == responses['empty_password']
    elif not data['valid_email']:
        assert signup_result == responses['invalid_email']
    elif email_exists:
        assert signup_result == responses['email_taken']
    elif not data['valid_password']:
        assert signup_result == responses['invalid_password']
    else:
        assert signup_result == responses['success']

browser.close()