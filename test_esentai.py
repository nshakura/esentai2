import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time



class EsentaiClient:

    EMAIL = 'admin@myesentai.com'
    PWD = '1'
    TITLE_BANNER = 'название баннера'

    def __init__(self, url):
        selenoid_url = 'http://127.0.0.1:4444/wd/hub'
        chrome_options = Options()
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Remote(
            command_executor=selenoid_url,
            desired_capabilities=chrome_options.to_capabilities(),
        )
        self.page = self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def is_visible(self, locator, by=By.XPATH, timeout=10):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def handle_error(self, err):
        raise Exception(err)

    def wait_for_element(self, locator, by, timeout=60):
        if self.is_visible(locator, by=by, timeout=timeout):
            return self.driver.find_element(by=by, value=locator)
        else:
            self.handle_error(f'Element {by} {locator} not found in {timeout}')

    def wait_for_element_by_id(self, locator, timeout=60):
        return self.wait_for_element(locator, By.ID, timeout=timeout)

    def wait_for_element_by_xpath(self, locator, timeout=60):
        return self.wait_for_element(locator, By.XPATH, timeout=timeout)

    def wait_for_element_by_css_selector(self, locator, timeout=60):
        return self.wait_for_element(locator, By.CSS_SELECTOR, timeout=timeout)

    def signin(self):
        self.wait_for_element_by_id("login").send_keys(self.EMAIL)
        self.wait_for_element_by_id("password").send_keys(self.PWD)
        self.wait_for_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)

    def is_signin_succeed(self):
        return self.is_visible("//span[contains(text(),'Статистика')]")

    def create_banner(self):
        self.wait_for_element_by_xpath("//span[contains(text(),'Кампании')]").click()
        self.wait_for_element_by_xpath("//a[@href='/campaigns/new']").click()
        self.wait_for_element_by_id("title").send_keys(self.TITLE_BANNER)
        self.wait_for_element_by_xpath("//input[@id='date_start']").click()
        self.wait_for_element_by_xpath("//span[contains(text(),'OK')]").click()
        time.sleep(3)
        self.wait_for_element_by_xpath("//input[@id='date_end']").click()
        self.wait_for_element_by_xpath("//span[contains(text(),'OK')]").click()
        self.wait_for_element_by_xpath("//span[contains(text(),'Перейти к настройке кампании')]").click()
        time.sleep(3)




class TestEsentai(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = EsentaiClient('https://app-test.myesentai.com')
        cls.client.signin()

    @classmethod
    def tearDownClass(cls):
        cls.client.quit()

    def test_signin(self):
        signin_succeed = self.client.is_signin_succeed()
        self.assertTrue(signin_succeed)
        l = self.client.create_banner()
        self.assertTrue(l)

