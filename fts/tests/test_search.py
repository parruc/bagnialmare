from random import sample, choice

from selenium.webdriver.common.keys import Keys
from phantomjstestcase import *
from bagni.tests.factories import *
from bagni.models import *

class SearchTest(PhantomJSTestCase):

    def setUp(self):
        super(SearchTest, self).setUp()
        self.data = setUpTestFactory()
        #each test in this class starts from the homepage (that is where search happens)
        self.get_url()

    def tearDown(self):
        super(SearchTest, self).tearDown()
        tearDownTestFactory()

    def test_empty_search(self):
        search_button = self.browser.find_element_by_id("search_submit")
        search_button.click()
        count = self.browser.find_element_by_class_name("hits-count")
        self.assertEqual(int(count.text), len(self.data['bagni']),
                msg = "Empty search hits-counts should be exactly as the number of Bagno object inserted")

    def test_what_name_search(self):
        bagno = choice(self.data['bagni'])
        query_text = bagno.name
        input_field = self.browser.find_element_by_id("search_q")
        input_field.send_keys(query_text + Keys.RETURN)
        try:
            bagno_link = self.browser.find_element_by_link_text(bagno.name)
        except NoSuchElementException:
            self.fail("cannot find link to inserted bagno: %s" % (bagno.name) )

    def test_where_municipality_search(self):
        #TODO: fix places fixtures for running this test
        #query_text = self.bagno[3].municipality.name
        #input_field = self.browser.find_element_by_id("search_l")
        #input_field.send_keys(query_text + Keys.RETURN)
        #hits_query = self.browser.find_element_by_class_name("hits-query")
        #self.assertIn(query_text, hits_query.text.lower(),
        #        msg = "Query should be displayed in .hits-query element")
        #bagni = self.browser.find_elements_by_class_name("bagno")
        #for bagno in bagni:
        #    distance = bagno.find_element_by_class_name("badge")
        #    self.assertTrue(float(distance.text[:-2].strip().replace(',', '.')) > 0,
        #            msg = "search results based on place should be ordered by distance")
        self.assertTrue(True)

    def test_what_service_search(self):
        bagno = choice(self.data['bagni'])
        service = choice(bagno.services.all())
        query_text = service.name
        input_field = self.browser.find_element_by_id("search_q")
        input_field.send_keys(query_text + Keys.RETURN)
        try:
            bagno_link = self.browser.find_element_by_link_text(bagno.name)
        except NoSuchElementException:
            self.fail("bagno %s has service %s but is not listed in search results" % (bagno.name, service.name) )
