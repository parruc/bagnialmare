from django.test import TestCase

from bagni.models import Bagno
from factories import *

class BagnoModelTest(TestCase):
    """
    What should we test in the models?
    """
    def setUp(self):
        """
        This already tests wether we can create a new object or not
        """
        self.added = BagnoFactory()

    def test_basic_retrival(self):
        """
        Does this test make any sense?
        """
        self.assertTrue(self.added in Bagno.objects.all())

    def test_index_features(self):
        """
        this test should definitely exist as it tests a method we added
        extending the basic django features.
        What should we test though?! If this test is a bare replication of the
        method defined in the model it makes no sense at all ...
        """
        b = Bagno.objects.all()[0]
        self.assertTrue(hasattr(b, 'index_features'))
        features = b.index_features()
        self.assertEqual(features['id'], unicode(b.id))
        self.assertTrue(features.has_key('text'))
        self.assertTrue(features.has_key('services'))


