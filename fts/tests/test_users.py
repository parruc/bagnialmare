from selenium.webdriver.common.keys import Keys

from phantomjstestcase import *
from bagni import search
from bagni.tests.factories import *

class TestUser(PhantomJSTestCase):
    def setUp(self):
        search.recreate_index()
        self.user = UserFactory()

    def tearDown(self):
        search.delete_index()

    def test_wrong_login(self):
        self.browser.get("%s%s" % (self.live_server_url, '/accounts/login/'))
        login_url = self.browser.current_url
        username_field = self.browser.find_element_by_id("id_login")
        username_field.send_keys("wronuser")
        password_field = self.browser.find_element_by_id("id_password")
        password_field.send_keys("wrongpassword")
        submit = self.browser.find_element_by_class_name("primaryAction")
        submit.click()
        self.assertEqual(self.browser.current_url, login_url)

    def test_login(self):
        self.browser.get("%s%s" % (self.live_server_url, '/accounts/login/'))
        login_url = self.browser.current_url
        username_field = self.browser.find_element_by_id("id_login")
        username_field.send_keys(self.user.username)
        password_field = self.browser.find_element_by_id("id_password")
        password_field.send_keys(DEFAULT_PASSWORD)
        submit = self.browser.find_element_by_class_name("primaryAction")
        submit.click()
        self.assertEqual(self.browser.title, u"Homepage")
