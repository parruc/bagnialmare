from django.test import LiveServerTestCase
from selenium import webdriver

class PhantomJSTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.PhantomJS(executable_path='/opt/phantomjs')
        #cls.browser.implicitly_wait(3)
        super(PhantomJSTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(PhantomJSTestCase, cls).tearDownClass()
