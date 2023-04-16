"""
                              GeneralPage -----------------
                                   |                      |
     SignInPageExtended------- SignInPage             PrivacyPolicy
              |                   |
      RegistrationPage      LoggedInPage -----------------
                                 |                       |
                         LoggedInMainPage         LoggedInUserPage
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
    # class with cookie elements for testing the privacy policy

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def cookie_panel(self) -> WebElement:
        return self.driver.find_element(By.ID, "cookie-policy-panel")

    def cookie_accept(self) -> WebElement:
        return self.driver.find_element(By.CLASS_NAME, "cookie__bar__buttons__button--accept")


class SignInPage(GeneralPage):
    # common elements for sign in function

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, url='http://localhost:1667/#/')

    def sign_in_link(self) -> WebElement:
        return self.driver.find_element(By.LINK_TEXT, "Sign in")

    def input_email(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Email"]')))

    def input_password(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//input[@placeholder="Password"]')

    def submit_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

    def logout_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//li/a[contains(text(), "Log out")]')))

    def signed_in_menu(self) -> WebElement:
        return self.wait().until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.nav-item:nth-child(4)')))


class SignInPageExtended(SignInPage):
    # Class derived from SignInPage with additional elements for testing sign in function

    def page_loaded(self) -> str:
        return self.wait().until(self.ECpoel((By.TAG_NAME, "h1"))).text

    def result_sign_in_failed(self) -> str:
        self.wait().until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="swal-title"]'), 'Login failed!'))
        return self.driver.find_element(By.XPATH, '//div[@class="swal-title"]').text

    def confirm_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')

    def info(self) -> str:
        return self.driver.find_element(By.XPATH, '//div[@class="swal-text"]').text


class RegistrationPage(SignInPageExtended):
    # Class derived from SignInPageExtended with additional elements for testing sign up function

    def sign_up_link(self) -> WebElement:
        return self.driver.find_element(By.LINK_TEXT, "Sign up")

    def input_username(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Username"]')))

    def result_registration_passed(self) -> WebElement:
        self.wait().until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="swal-title"]'), 'Welcome!'))
        return self.wait().until(self.ECpoel((By.XPATH, '//div[@class="swal-title"]'))).text

    def result_registration_failed(self) -> str:
        self.wait().until(
            EC.text_to_be_present_in_element((By.XPATH, '//div[@class="swal-title"]'), 'Registration failed!'))
        return self.driver.find_element(By.XPATH, '//div[@class="swal-title"]').text


class LoggedInPage(SignInPage):
    # Common elements of main page after successful log in

    # def articles_favorite_buttons(self) -> list[WebElement]:
    #     return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='article-meta']/button")))

    # def articles_own_tags(self) -> list[WebElement]:
    #     return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='article-preview']/a/div/a")))

    def articles_titles(self) -> list[WebElement]:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='article-preview']/a/h1")))

    def articles_abouts(self) -> list[WebElement]:
        return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='article-preview']/a/p")))

    def first_article_title(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, "//div/a/h1")))


class LoggedInUserPage(LoggedInPage):
    # Class derived from LoggedInPage with elements of user menu

    def my_articles(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.LINK_TEXT, 'My Articles')))

    def no_articles_yet(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, "//div[@class='article-preview']")))

    # creating/modifying/delete articles section
    def create_article_link(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.CSS_SELECTOR, '.nav-item:nth-child(2)')))

    def input_article_title(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//input[@placeholder="Article Title"]')))

    def input_article_about(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')

    def input_article_body(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')

    def input_article_tags(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//input[@placeholder="Enter tags"]')

    def publish_button(self) -> WebElement:
        return self.driver.find_element(By.XPATH, '//button[@type="submit"]')

    def modify_article_link(self) -> WebElement:
        return self.wait().until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-sm btn-outline-secondary"]')))

    def delete_article_button(self) -> WebElement:
        return self.wait().until(self.ECpoel((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))


class LoggedInMainPage(LoggedInPage):
    # Class derived from LoggedInPage with additional elements of main page after successful log in

    # def popular_tags(self) -> list[WebElement]:
    #     return self.wait().until(self.ECpoels((By.XPATH, "//div[@class='sidebar']/div/a")))

    def pagination(self) -> list[WebElement]:
        return self.wait().until(self.ECpoels((By.XPATH, "//ul[@class='pagination']/li")))

    def pagination_links(self) -> list[WebElement]:
        return self.wait().until(self.ECpoels((By.XPATH, "//ul[@class='pagination']/li/a")))
