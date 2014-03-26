from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

PHANTOMJS_PATH = '/opt/phantomjs'
import os
if not os.path.exists(PHANTOMJS_PATH):
    print "You can download phantomjs from https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-i686.tar.bz2"
    print "extract it and place the executable in /opt"
    print "reme,ber to set it executable by user ombrelloni"
    raise IOError("cannot find phantomjs executable at: %s" % (PHANTOMJS_PATH,))

class PhantomJSTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = None
        super(PhantomJSTestCase, cls).setUpClass()

    def setUp(self):
        self._init_browser()

    def tearDown(self):
        self._close_browser()

    def _init_browser(self):
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
        self.browser.implicitly_wait(3)

    def _close_browser(self):
        self.browser.quit()

    def get_url(self, url_path = ""):
        self.browser.get(self.live_server_url + url_path)

    def assertContainsXpath(self, xpath, msg_prefix=None):
        """
        check wether the element identified by the given xpath is contained in the html page pointed
        by the integrated phantomjs browser
        @param xpath: string representation of the element xpath
        @param msg_prefix: custom error message displayed as test result in case of failure
        """
        try:
            self.browser.find_element_by_xpath(xpath)
        except WebDriverException, wde:
            if msg_prefix:
                msg = msg_prefix
            else:
                #if we did not set any error message, take it from the library
                msg = wde.msg
            self.fail(msg)
