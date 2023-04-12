"""
                              GeneralPage -----------------
                                   |                      |
               -------------- SignInPage             PrivacyPolicy
              |                   |
      RegistrationPage     LoggedInUserPage
                                 |
                         LoggedInMainPage
"""

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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


class PrivacyPolicy(GeneralPage):

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def cookie_panel(self) -> WebElement:
        return self.driver.find_element(By.ID, "cookie-policy-panel")

    def cookie_accept(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.CLASS_NAME, "cookie__bar__buttons__button--accept")))


class SignInPage(GeneralPage):

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def sign_in_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.LINK_TEXT, "Sign in")))

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

    def signed_in_menu(self, index) -> WebElement | str:
        return self.wait().until(self.ECpoels((By.XPATH, '//li[@class="nav-item"]/a')))[index]

    # no lag version
    # def signed_in_link(self) -> WebElement:
    #     return self.wait().until(self.ECpoel((By.XPATH, f'//li/a[contains(text(), "{active_user["username"]}")]'))).text

    def logout_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//li/a[contains(text(), "Log out")]')))


class RegistrationPage(SignInPage):

    def sign_up_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.LINK_TEXT, "Sign up")))

    def input_username(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Username"]')))


class LoggedInUserPage(SignInPage):

    def user_articles_tabs(self, index) -> list:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='articles-toggle']/ul/li/a")))[index]

    def articles_titles(self) -> WebElement | list:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='article-preview']/a/h1")))

    def articles_own_tags(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "//a[@class='preview-link']/div/a")))

    def articles_favorite_buttons(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "div[@class='article-meta']/button")))

    def no_articles_yet(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, "//div[@class='article-preview']")))

    # creating/modifying/delete articles section
    def new_article_link(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, '//li[@class="nav-item"]/a')))[1]

    def article_title(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Article Title"]')))

    def article_about(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="What\'s this article about?"]')))

    def article_body(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')))

    def article_tags(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Enter tags"]')))

    def publish_button(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//button[@type="submit"]')))

    def modify_article_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//a[@class="btn btn-sm btn-outline-secondary"]')))

    def delete_article_button(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))


class LoggedInMainPage(LoggedInUserPage):

    def main_articles_tabs(self) -> WebElement:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='feed-toggle']/ul/li")))

    def popular_tags(self) -> list:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='sidebar']/div/a")))

    def pagination(self) -> list:
        return self.wait().until(self.ECpoels((By.XPATH, "//ul[@class='pagination']/li")))

    def pagination_links(self) -> list:
        return self.wait().until(self.ECpoels((By.XPATH, "//ul[@class='pagination']/li/a")))
