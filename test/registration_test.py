import allure
import csv
import bcrypt
import configuration as config
from registration_model import RegistrationPage

valid_user = {
    'username': 'Béla',
    'email': 'abc@abcd1.bc',
    'password': 'HJkksdfjdvb4'
}


class TestRegistration:

    def setup_method(self):
        self.page = RegistrationPage(driver=config.get_preconfigured_chrome_driver())
        self.page.open()
        self.page.signup_page().click()

    def teardown_method(self):
        self.page.close()

    # @allure
    def test_signup_page_loaded(self):
        assert self.page.signup_page_loaded() == 'Sign up'

    def test_signup_with_valid_data(self):
        self.page.input_username().send_keys(valid_user['username'])
        self.page.input_email().send_keys(valid_user['email'])
        self.page.input_password().send_keys(valid_user['password'])
        self.page.submit_button().click()
        assert self.page.registration_result() == "Welcome!"
        assert self.page.registration_info() == "Your registration was successful!"

    def test_valid_signup_on_backend(self):
        id_db, username_db, pass_hashed_db, email_db, *_ = self.page.query_db(
            f"SELECT * FROM users WHERE email = '{valid_user['email']}'")[0]
        encoded_hash = pass_hashed_db.encode()
        encoded_password = valid_user['password'].encode()
        assert valid_user['username'] == username_db
        assert valid_user['email'] == email_db
        assert bcrypt.checkpw(encoded_password, encoded_hash)

    def test_signup_with_registered_email(self):
        self.page.input_username().send_keys(valid_user['username'])
        self.page.input_email().send_keys(valid_user['email'])
        self.page.input_password().send_keys(valid_user['password'])
        self.page.submit_button().click()
        assert self.page.registration_result() == "Registration failed!"
        assert self.page.registration_info() == "Email already taken."

    def test_signup_with_invalid_data(self):
        with open('data.csv', 'r', encoding='UTF-8') as file:
            testdata = csv.reader(file)
            next(testdata)
            for row in testdata:
                self.page.input_username().send_keys(row[0])
                self.page.input_email().send_keys(row[1])
                self.page.input_password().send_keys(row[2])
                self.page.submit_button().click()
                assert self.page.registration_result() == row[3]
                assert self.page.registration_info() == row[4]
                self.page.confirm_button().click()
        with open('alma.txt', "w") as f:
            f.write("alma")
