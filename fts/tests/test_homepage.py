from selenium.webdriver.common.keys import Keys
from phantomjstestcase import *
from bagni import search

class HomePageTest(PhantomJSTestCase):

    def setUp(self):
        super(HomePageTest, self).setUp()
        search.recreate_index()
        #each test in this class starts from the homepage
        self.get_url()

    def tearDown(self):
        super(HomePageTest, self).tearDown()
        search.delete_index()

    def test_home_page_title(self):
        self.assertEqual(self.browser.title, "Homepage", msg="This test is stupid")

    def test_home_page_form_fields(self):
        self.assertContainsXpath("//input[@id='search_q']", "homepage should contain input field with id: search_q")
        self.assertContainsXpath("//input[@id='search_l']", "homepage should contain input field with id: search_l")
        self.assertContainsXpath("//button[@id='search_submit']", "homepage should contain button field with id: search_submit")

    def test_home_page_contains_copyright(self):
        self.assertIn("copyright", self.browser.page_source.lower(),
                msg = "homepage should contain some copyright notice")

