from random import choice
from selenium.webdriver.common.keys import Keys

from phantomjstestcase import *
from bagni import search
from bagni.tests.factories import *

class TestUser(PhantomJSTestCase):

    def setUp(self):
        super(TestUser, self).setUp()
        self.data = setUpTestFactory()

    def tearDown(self):
        super(TestUser, self).tearDown()
        tearDownTestFactory()

    def test_login_page_contains_signup_link(self):
        self.get_url("/accounts/login/")
        self.assertContainsXpath("//a[contains(@href, '/accounts/signup/')]",
                msg_prefix = "login page should contain a link to signup page")

    def test_user_signup_correct(self):
        self._compile_signup_form()
        self.assertContainsXpath("//ul[@class='messages']/li[contains(@class,'alert-success')]",
                msg_prefix = "could not signup new user. Redirect page should contain success message.")

    def test_user_signup_wrong_password_check(self):
        self._compile_signup_form(password2="wrongcheckpassword")
        self.assertContainsXpath("//ul[@class='errorlist']/li",
                msg_prefix = "There should be an item in the error list related to the wrong password check")

    def test_user_signup_wrong_privacy_check(self):
        self._compile_signup_form(privacy=False)
        self.assertContainsXpath("//ul[@class='errorlist']/li",
                msg_prefix = "There should be an item in the error list related to the wrong privacy check")

    def test_user_signup_empty_username(self):
        self._compile_signup_form(username="")
        self.assertContainsXpath("//ul[@class='errorlist']/li",
                msg_prefix = "There should be an item in the error list related to the empty username")

    def test_user_signup_invalid_email(self):
        self._compile_signup_form(email="thi.is.not.--valid.com")
        self.assertContainsXpath("//ul[@class='errorlist']/li",
                msg_prefix = "There should be an item in the error list related to the invalid email")

    def test_wrong_login(self):
        self.get_url('/accounts/login/')
        login_url = self.browser.current_url
        username_field = self.browser.find_element_by_id("id_login")
        username_field.send_keys("wronguser")
        password_field = self.browser.find_element_by_id("id_password")
        password_field.send_keys("wrongpassword")
        submit = self.browser.find_element_by_class_name("primaryAction")
        submit.click()
        self.assertEqual(self.browser.current_url, login_url)

    def test_login(self):
        self.get_url('/accounts/login/')
        login_url = self.browser.current_url
        username_field = self.browser.find_element_by_id("id_login")
        username_field.send_keys(self.data['normal_user'].username)
        password_field = self.browser.find_element_by_id("id_password")
        password_field.send_keys(DEFAULT_PASSWORD)
        password_field.submit()
        self.assertEqual(self.browser.title, u"Homepage")

    def _compile_signup_form(self, username="newuser1",
                                   privacy = True,
                                   email="newuser1@example.com",
                                   password1="newpassword",
                                   password2="newpassword"):
        self.get_url("/accounts/signup/")
        form_element = self.browser.find_element_by_xpath("//form[@id='signup_form']")
        bagno_select = form_element.find_element_by_id("id_bagni")
        bagno_options = bagno_select.find_elements_by_tag_name("option")
        chosen_option = choice(bagno_options)
        chosen_option.click()
        username_field = form_element.find_element_by_id(u"id_username")
        username_field.send_keys(username)
        privacy_field = form_element.find_element_by_id(u"id_privacy")
        if privacy_field.is_selected():
            if not privacy:
                privacy_field.click()
        else:
            if privacy:
                privacy_field.click()
        email_field = form_element.find_element_by_id(u"id_email")
        email_field.send_keys(email)
        password_field = form_element.find_element_by_id(u"id_password1")
        password_field.send_keys(password1)
        password2_field = form_element.find_element_by_id(u"id_password2")
        password2_field.send_keys(password2)
        password2_field.submit()
