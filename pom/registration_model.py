import psycopg2 as pg

from general_model import GeneralPage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class RegistrationPage(GeneralPage):

    def __init__(self, driver: Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def signup_page(self):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Sign up")))

    def signup_page_loaded(self):
        return self.driver.find_element(By.TAG_NAME, "h1").text

    def input_username(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Username"]')))

    def input_email(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email"]')))

    def input_password(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Password"]')))

    def submit_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))

    def registration_result(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]'))).text

    def registration_info(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text

    def confirm_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))

    def query_db(self, sql):
        conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
