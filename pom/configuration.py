import psycopg2 as pg

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_preconfigured_chrome_driver() -> webdriver.Chrome:
    s = Service(executable_path=ChromeDriverManager().install())
    o = Options()
    o.add_experimental_option('detach', True)
    o.add_argument('window-position=500,0')
    # o.add_argument("--lang=en")
    # o.add_argument('--headless')
    # o.add_argument('--no-sandbox')
    # o.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(service=s, options=o)

def query_db(sql):
    conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# def query_db(sql):
#     conn = pg.connect("dbname='realworld' user='user' password='userpassword' host='localhost' port='54320'")
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.close()
#     return rows


# Csak példa a funkció használatára.
# Más modulba importálva ez a rész nem fog lefutni.
# if __name__ == '__main__':

    # driver = get_preconfigured_chrome_driver()
    # driver.get('https://www.progmasters.hu')
    #
    # driver.maximize_window()

