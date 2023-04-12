# (*) Regisztráció
# (*) Bejelentkezés
# (*) Adatkezelési nyilatkozat használata
# (*) Adatok listázása
# (*) Több oldalas lista bejárása
# (*) Új adat bevitel
# (*) Ismételt és sorozatos adatbevitel adatforrásból
# (*) Meglévő adat módosítás
# (*) Adat vagy adatok törlése
# Adatok lementése felületről
# (*) Kijelentkezés

import time
import allure
import bcrypt
from selenium.common import NoSuchElementException, TimeoutException
import configuration as config
from page_objects import RegistrationPage, SignInPage, PrivacyPolicy, LoggedInMainPage, LoggedInUserPage
from general_functions import *


class TestRegistration:

    def setup_method(self):
        self.page = RegistrationPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        assert self.page.sign_up_link().is_displayed()
        self.page.sign_up_link().click()
        assert self.page.page_loaded() == 'Sign up'

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-01")
    @allure.title("Sign up with valid user data")
    def test_sign_up_with_valid_data(self):
        for user in get_users_from_file("valid_user"):
            username, email, password, expected_result, expected_info, *_ = user
            user_registration(self.page, username, email, password)
            assert self.page.result() == expected_result
            assert self.page.info() == expected_info
            set_active_user(username, email, password)
            allure.dynamic.description(f'Registered user:\nUsername: {username}\nE-mail: {email}\nPassword: {password}')

    @allure.id("ATC-02")
    @allure.title("Checking sign up data stored in database")
    def test_valid_signup_data_in_database(self):
        for user in get_users_from_file("valid_user"):
            username, email, password, *_ = user
            sql = f"SELECT username, password, email FROM users WHERE email = '{email}'"
            username_from_db, pass_hashed_from_db, email_from_db = database_query(sql)[0]
            encoded_hash = pass_hashed_from_db.encode()
            encoded_password = password.encode()
            assert username == username_from_db
            assert email == email_from_db
            assert bcrypt.checkpw(encoded_password, encoded_hash)

    @allure.id("ATC-03")
    @allure.title("Sign up with already registered user data")
    def test_signup_with_registered_email(self):
        for user in get_users_from_file("valid_user"):
            username, email, password, *_ = user
            user_registration(self.page, username, email, password)
            assert self.page.result() == "Registration failed!"
            assert self.page.info() == "Email already taken."

    @allure.id("ATC-04")
    @allure.title("Sign up with invalid user data")
    def test_signup_with_invalid_data(self):
        for user in get_users_from_file("invalid_user"):
            username, email, password, expected_result, expected_info, *_ = user
            user_registration(self.page, username, email, password)
            assert self.page.result() == expected_result
            assert self.page.info() == expected_info
            self.page.confirm_button().click()


class TestSignIn:

    def setup_method(self):
        self.page = SignInPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        assert self.page.sign_in_link().is_displayed()
        self.page.sign_in_link().click()
        assert self.page.page_loaded() == 'Sign in'

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-05")
    @allure.title("Sign in with invalid user data")
    def test_sign_in_with_invalid_data(self):
        for user in get_users_from_file("invalid_login"):
            _, email, password, expected_result, expected_info, *_ = user
            user_login(self.page, email, password)
            time.sleep(0.1)
            assert self.page.result() == expected_result
            assert self.page.info() == expected_info
            self.page.confirm_button().click()

    @allure.id("ATC-06")
    @allure.title("Sign in and sign out with valid user data")
    def test_sign_out(self):
        user = get_active_user()
        user_login(self.page, user["email"], user["password"])
        assert self.page.signed_in_menu(3).text == user["username"]
        assert self.page.logout_link().is_displayed()
        self.page.logout_link().click()
        assert self.page.sign_in_link().is_displayed()


class TestPrivacyPolicy:

    def setup_method(self):
        self.page = PrivacyPolicy(driver=config.get_preconfigured_chrome_driver())
        self.page.open()

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-07")
    @allure.title("Checking Privacy Policy")
    def test_cookie_accept(self):
        assert self.page.cookie_panel().is_displayed()
        self.page.cookie_accept().click()
        time.sleep(.5)
        try:
            assert self.page.cookie_panel().is_displayed()
        except NoSuchElementException:
            allure.dynamic.description("After clicking on 'Accept' button cookie panel disappears.")


class TestLoggedInMainPage:

    def setup_method(self):
        self.page = LoggedInMainPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        assert self.page.sign_in_link().is_displayed()
        self.page.sign_in_link().click()
        user = get_active_user()
        user_login(self.page, user["email"], user["password"])
        assert self.page.logout_link().is_displayed()

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-08")
    @allure.title("Checking page list traversal")
    def test_page_list_traversal(self):
        pagination = self.page.pagination()
        page_links = self.page.pagination_links()
        for index, page_link in enumerate(page_links):
            page_link.click()
            assert page_link.text == str(index + 1)
            assert pagination[index].get_attribute("class") == "page-item active"
            assert pagination[index].get_attribute("data-test") == f"page-link-{index + 1}"

    @allure.id("ATC-09")
    @allure.title("Listing all article titles")
    def test_list_articles(self):
        articles = self.page.articles_titles()
        articles_titles = ""
        for article in articles:
            articles_titles += f'{article.text}\n'
        allure.dynamic.description(f'List of articles: \n{articles_titles}')


class TestLoggedInUserPage:

    def setup_method(self):
        self.page = LoggedInUserPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        assert self.page.sign_in_link().is_displayed()
        self.page.sign_in_link().click()
        user = get_active_user()
        user_login(self.page, user["email"], user["password"])
        assert self.page.logout_link().is_displayed()
        self.page.signed_in_menu(3).click()
        time.sleep(2)

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-10")
    @allure.title("Creating articles from csv file")
    def test_creating_articles(self):
        titles = create_articles_from_file(self.page)
        self.page.signed_in_menu(3).click()
        for index, title in enumerate(titles):
            assert self.page.articles_titles()[index].text == title
        allure.dynamic.description(f"Created articles:\n{' ,'.join(titles)}")

    @allure.id("ATC-11")
    @allure.title("Modifying article")
    def test_modifying_article(self):
        modified_title = modify_title(self.page)
        assert self.page.articles_titles()[-1].text == modified_title

    @allure.id("ATC-12")
    @allure.title("Deleting all created articles")
    def test_deleting_articles(self):
        self.page.refresh()
        articles = len(self.page.articles_titles())
        for index in range(articles):
            self.page.articles_titles()[0].click()
            self.page.delete_article_button().click()
            time.sleep(1)
            self.page.signed_in_menu(3).click()
            time.sleep(2)
        assert self.page.no_articles_yet().text == "No articles are here... yet."





