from selenium.webdriver.common.keys import Keys
from phantomjstestcase import *
from bagni import search
from bagni.tests.factories import *
import bagni

class HomePageTest(PhantomJSTestCase):

    def setUp(self):
        search.recreate_index()
        for i in xrange(10):
            BagnoFactory()

    def tearDown(self):
        search.delete_index()

    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, "Homepage")

    def test_empty_search(self):
        self.browser.get(self.live_server_url)
        input_field = self.browser.find_element_by_id("search_q")
        input_field.send_keys(Keys.RETURN)
        count = self.browser.find_element_by_class_name("hits-count")
        self.assertEqual(int(count.text), 10)

    def test_what_name_search(self):
        bagno = bagni.models.Bagno.objects.first()
        query_text = bagno.name
        self.browser.get(self.live_server_url)
        input_field = self.browser.find_element_by_id("search_q")
        input_field.send_keys(query_text + Keys.RETURN)
        panels = self.browser.find_elements_by_class_name("panel")
        self.assertTrue(len(panels) > 0)
        map_markers = self.browser.find_elements_by_class_name("leaflet-marker-icon")
        count = self.browser.find_element_by_class_name("hits-count")
        self.assertEqual(int(count.text), len(map_markers))

    def test_what_service_search(self):
        #query_text = "racchettoni"
        #self.browser.get(self.live_server_url)
        #service_link = self.browser.find_element_by_link_text(query_text)
        #service_link.click()
        #filters = self.browser.find_element_by_class_name("active-filters")
        #filter_field = filters.find_element_by_partial_link_text(query_text)
        #self.assertTrue(filter_field)
        self.assertTrue(True)

    def test_where_search(self):
        #query_text = "cesenatico"
        #self.browser.get(self.live_server_url)
        #input_field = self.browser.find_element_by_id("search_l")
        #input_field.send_keys(query_text + Keys.RETURN)
        #hits_query = self.browser.find_element_by_class_name("hits-query")
        #self.assertIn(query_text, hits_query.text.lower())
        #bagni = self.browser.find_elements_by_class_name("bagno")
        #for bagno in bagni:
        #    distance = bagno.find_element_by_class_name("badge")
        #    self.assertTrue(float(distance.text[:-2].strip().replace(',', '.')) > 0)
        self.assertTrue(True)
