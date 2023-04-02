# Regisztráció ***
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
import bcrypt
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def query_db(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


#  check backend data records and password hash on successful registration
def check_registration_data_in_db(user, email, password):
    id_db, username_db, pass_hashed_db, email_db, *_ = query_db(
        f"SELECT * FROM users WHERE email = '{email}'")[0]

    print(f'SQL result:\nID: {id_db}\nUsername: {username_db}\nE-mail: '
          f'{email_db}\nPassword: {password}\nHash: {pass_hashed_db}')

    encoded_hash = pass_hashed_db.encode()  # encoding needed to array of bytes
    encoded_password = password.encode()  # encoding needed to array of bytes
    assert user == username_db
    assert email == email_db
    assert bcrypt.checkpw(encoded_password, encoded_hash)  # comparing password with hashed string


# class TestRegistration(object):
#     def setup_method(self):
#         service = Service(executable_path=ChromeDriverManager().install())
#         options = Options()
#         options.add_experimental_option("detach", True)
#         options.add_argument("--lang=en")
#         self.browser = webdriver.Chrome(service=service, options=options)
#         # self.browser.implicitly_wait(10)
#         URL = "http://localhost:1667/#/"
#         self.browser.get(URL)
#
#     def teardown_method(self):
#         self.browser.quit()
#
#     def click_signup_page(self):
#         register = self.browser.find_element(By.LINK_TEXT, "Sign up")
#         register.click()

    # def sign_up(self, user, email, password):
    #     find = self.browser.find_element
    #     self.click_signup_page()
    #
    #     input_username = find(By.XPATH, '//input[@placeholder="Username"]')  # let's dance!
    #     input_email = find(By.XPATH, '//input[@placeholder="Email"]')
    #     input_password = find(By.XPATH, '//input[@placeholder="Password"]')
    #     submit_btn = find(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    #     input_username.send_keys(user)
    #     input_email.send_keys(email)
    #     input_password.send_keys(password)
    #     submit_btn.click()
    #
    #     reg_result = WebDriverWait(self.browser, 5).until(
    #         EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]'))).text
    #     reg_info = find(By.XPATH, '//div[@class="swal-text"]').text
    #     confirm_btn = find(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
    #     confirm_btn.click()
    #     return f'{reg_result} {reg_info}'

    # def test_signup_page_loaded(self):
    #     self.click_signup_page()
    #     signup_page_check = self.browser.find_element(By.TAG_NAME, "h1").text
    #     assert signup_page_check == 'Sign up'

    # checking the 'have an account link' leads to sign-in page
    def test_link_to_sign_in(self):
        self.click_signup_page()
        link_sign_in = self.browser.find_element(By.LINK_TEXT, "Have an account?")
        link_sign_in.click()
        sign_in_page_check = self.browser.find_element(By.TAG_NAME, "h1").text
        assert sign_in_page_check == 'Sign in'

    def test_fill_registration_form(self):
        #  read test data from file 'registration_data.json'
        with open("registration_data.json", "r", encoding="UTF-8") as reg_data:
            test_data = json.loads(reg_data.read())
        #  read web responses from file 'web_responses.json'
        with open("web_responses.json", "r", encoding="UTF-8") as web_resp:
            responses = json.loads(web_resp.read())

        for data in test_data:
            email_exists = query_db(f"SELECT email FROM users WHERE email = '{data['email']}'")
            signup_result = self.sign_up(data['user'], data['email'], data['password'])

            print(f"user: {data['user']}, mail: {data['email']}, pass: {data['password']}")
            print(signup_result)
            print()

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
                assert signup_result == responses['success']  # on success let's check the backend
                check_registration_data_in_db(data['user'], data['email'], data['password'])
