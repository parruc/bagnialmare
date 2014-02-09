from django.test import TestCase
from bagni.models import Bagno
from factories import *

class HomePage(TestCase):
    """
    Very very simple test case. Just shows how to use the client.get method
    """
    def test_home_page_template(self):
        self.assertTrue(len(Bagno.objects.all()) == 0) #true if no fixture
        response = self.client.get("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "bagni/homepage.html")

class BagniPage(TestCase):
    """
    Let's begin to create stuff and test the database functionalities and view
    argument passing
    """

    def setUp(self):
        for i in xrange(20):
            BagnoFactory.create()

    def test_view_params(self):
        self.assertTrue(len(Bagno.objects.all()) > 10) #false if fixtures
        response = self.client.get('/bagni/', follow=True)
        self.assertIn('object_list', response.context)

class Login(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_registered_user_login(self):
        logged_in = self.client.login(username = self.user.username,
                password = DEFAULT_PASSWORD)
        self.assertTrue(logged_in)

    def test_unregistered_user_login(self):
        logged_in = self.client.login(username = "utenteinesistente",
                password = "passwordcasuale")
        self.assertFalse(logged_in)

class BagnoEditPage(TestCase):
    def setUp(self):
        self.normal_user = UserFactory()
        self.bagno = BagnoFactory()
        self.manager_user = ManagerFactory.create(bagni=(self.bagno,))
        self.wrong_manager = ManagerFactory.create(bagni=(BagnoFactory(),))
        #self.admin = UserFactory()
        #self.admin.is_staff = True

    def test_edit_without_login(self):
        resp = self.client.get(self.bagno.get_absolute_url() + "edit/", follow=True)
        self.assertEqual(resp.status_code, 403)

    def test_normal_user_attempt_edit(self):
        self.client.login(username = self.normal_user.username,
                password = DEFAULT_PASSWORD)
        resp = self.client.get(self.bagno.get_absolute_url() + "edit/", follow=True)
        self.assertEqual(resp.status_code, 403)

    def test_manager_attempt_edit(self):
        self.client.login(username = self.manager_user.user.username,
                password = DEFAULT_PASSWORD)
        resp = self.client.get(self.bagno.get_absolute_url() + "edit/", follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_wrong_manager_attempt_edit(self):
        self.client.login(username = self.wrong_manager.user.username,
                password = DEFAULT_PASSWORD)
        resp = self.client.get(self.bagno.get_absolute_url() + "edit/", follow=True)
        self.assertEqual(resp.status_code, 403)

    #def test_admin_attempt_edit(self):
    #    self.client.login(username = self.admin.username,
    #            password = DEFAULT_PASSWORD)
    #    resp = self.client.get(self.bagno.get_absolute_url() + "edit/", follow=True)
    #    self.assertEqual(resp.status_code, 200)

