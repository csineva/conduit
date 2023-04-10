"""
                        GeneralPage -------------------
                             |                        |
                   -- ConduitMainPage --         PrivacyPolicy
                  |                    |
             SignInPage         LoggedInUserPage
                 |                    |
         RegistrationPage      LoggedInMainPage
"""



from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from general_functions import active_user


class GeneralPage:

    def __init__(self, driver: webdriver.Chrome, url):
        self.driver = driver
        self.url = url
        self.ECpoel = EC.presence_of_element_located
        self.ECpoels = EC.presence_of_all_elements_located

    def wait(self, sec=5):
        return WebDriverWait(self.driver, sec)

    def open(self):
        self.driver.get(self.url)

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()


class ConduitMainPage(GeneralPage):

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def sign_in_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.LINK_TEXT, "Sign in")))


class SignInPage(ConduitMainPage):

    def page_loaded(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.TAG_NAME, "h1"))).text

    def input_email(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Email"]')))

    def input_password(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Password"]')))

    def submit_button(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))

    def result(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//div[@class="swal-title"]'))).text

    def info(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//div[@class="swal-text"]'))).text

    def confirm_button(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))

    def signed_in_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, f'//li/a[contains(text(), "{active_user["username"]}")]'))).text

    def logout_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//li/a[contains(text(), "Log out")]')))


class RegistrationPage(SignInPage):

    def sign_up_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.LINK_TEXT, "Sign up")))

    def input_username(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Username"]')))


class PrivacyPolicy(GeneralPage):

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def cookie_panel(self) -> WebElement:
        return self.driver.find_element(By.ID, "cookie-policy-panel")

    def cookie_accept(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.CLASS_NAME, "cookie__bar__buttons__button--accept")))


class LoggedInUserPage(ConduitMainPage):

    def user_page_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, f'//li/a[contains(text(), "{active_user["username"]}")]'))).text

    def articles_titles(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "a[@class='preview-link']/h1")))

    def articles_own_tags(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "a[@class='preview-link']/div")))

    def articles_favorite_buttons(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "div[@class='article-meta']/button")))

    def user_articles_tabs(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='articles-toggle']/ul/li")))


class LoggedInMainPage(LoggedInUserPage):

    def main_articles_tabs(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='feed-toggle']/ul/li")))

    def popular_tags(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='sidebar']/div/a")))

    def pagination(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "ul[@class='pagination']/li")))