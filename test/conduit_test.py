# (*) Regisztráció
# (*) Bejelentkezés
# (*) Adatkezelési nyilatkozat használata
# Adatok listázása
# Több oldalas lista bejárása
# Új adat bevitel
# (*) Ismételt és sorozatos adatbevitel adatforrásból
# Meglévő adat módosítás
# Adat vagy adatok törlése
# Adatok lementése felületről
# (*) Kijelentkezés

import time
import allure
import bcrypt
from selenium.common import NoSuchElementException
import configuration as config
from page_objects import RegistrationPage, SignInPage, PrivacyPolicy
from general_functions import user_registration, user_login, database_query, get_user, active_user


class TestRegistration:

    def setup_method(self):
        self.page = RegistrationPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        assert self.page.sign_up_link().is_displayed()
        self.page.sign_up_link().click()

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-01")
    @allure.title("Ellenőrizzük, hogy megnyílt a regisztrációs oldal")
    def test_sign_up_page_loaded(self):
        assert self.page.page_loaded() == 'Sign up'

    @allure.id("ATC-02")
    @allure.title("Regisztráció érvényes felhasználó adatokkal")
    def test_sign_up_with_valid_data(self):
        for user in get_user("valid_user"):
            username, email, password, expected_result, expected_info, *_ = user
            user_registration(self.page, username, email, password)
            assert self.page.result() == expected_result
            assert self.page.info() == expected_info
            # active_user["username"] = username
            # active_user["email"] = email
            # active_user["password"] = password

    @allure.id("ATC-03")
    @allure.title("Ellenőrizzük, hogy a sikeres regisztráció adatai rögzítésre kerültek az adatbázisban")
    def test_valid_signup_data_in_database(self):
        for user in get_user("valid_user"):
            username, email, password, *_ = user
            sql = f"SELECT username, password, email FROM users WHERE email = '{email}'"
            username_from_db, pass_hashed_from_db, email_from_db = database_query(sql)[0]
            encoded_hash = pass_hashed_from_db.encode()
            encoded_password = password.encode()
            assert username == username_from_db
            assert email == email_from_db
            assert bcrypt.checkpw(encoded_password, encoded_hash)

    @allure.id("ATC-04")
    @allure.title("Regisztráció korábban már regisztrált felhasználó adataival")
    def test_signup_with_registered_email(self):
        """Regisztrált maillel teszt"""
        for user in get_user("valid_user"):
            username, email, password, *_ = user
            user_registration(self.page, username, email, password)
            assert self.page.result() == "Registration failed!"
            assert self.page.info() == "Email already taken."

    @allure.id("ATC-05")
    @allure.title("Regisztráció ellenőrzése érvénytelen felhasználói adatokkal")
    def test_signup_with_invalid_data(self):
        for user in get_user("invalid_user"):
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

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-06")
    @allure.title("Ellenőrizzük, hogy megnyílt a Login oldal")
    def test_sign_in_page_loaded(self):
        assert self.page.page_loaded() == 'Sign in'

    @allure.id("ATC-07")
    @allure.title("Bejelentkezés ellenőrzése érvénytelen felhasználói adatokkal")
    def test_sign_in_with_invalid_data(self):
        for user in get_user("invalid_login"):
            _, email, password, expected_result, expected_info, *_ = user
            user_login(self.page, email, password)
            time.sleep(0.1)
            assert self.page.result() == expected_result
            assert self.page.info() == expected_info
            self.page.confirm_button().click()

    @allure.id("ATC-08")
    @allure.title("Bejelentkezés érvényes, már regisztrált felhasználói adattal")
    def test_sign_in_with_valid_data(self):
        user_login(self.page)
        assert self.page.signed_in_link() == active_user["username"]
        assert self.page.logout_link().is_displayed()

    @allure.id("ATC-09")
    @allure.title("Bejelentkezés után kijelentkezés")
    def test_sign_out(self):
        user_login(self.page)
        assert self.page.signed_in_link() == active_user["username"]
        self.page.logout_link().click()
        assert self.page.sign_in_link().is_displayed()


class TestPrivacyPolicy:

    def setup_method(self):
        self.page = PrivacyPolicy(driver=config.get_preconfigured_chrome_driver())
        self.page.open()

    def teardown_method(self):
        self.page.close()

    @allure.id("ATC-10")
    @allure.title("Adatkezelési nyilatkozat ellenőrzése")
    def test_cookie_accept(self):
        assert self.page.cookie_panel().is_displayed()
        self.page.cookie_accept().click()
        time.sleep(1)
        try:
            assert self.page.cookie_panel().is_displayed()
        except NoSuchElementException:
            print("\nAs accepted, cookie panel disappears.")


