import json

from django.test import TestCase

from factories import NewsletterTemplateFactory
from factories import NewsletterTargetFactory
from factories import NewsletterSubscriptionFactory
from factories import NewsletterFactory
from factories import UserFactory
from newsletters import models

class NewsletterTest(TestCase):
    """
    Test if we get errors sending the Newsletter
    """
    def setUp(self):
        """
        This already tests wether we can create a new object or not
        """
        self.newsletter_template = NewsletterTemplateFactory()
        self.newsletter_targets = [NewsletterTargetFactory(name="Target 1"), NewsletterTargetFactory(name="Target 2")]
        self.newsletters = [NewsletterFactory(target=self.newsletter_targets[0]),
                            NewsletterFactory(target=self.newsletter_targets[1]), ]
        self.subscriptions = [NewsletterSubscriptionFactory(email="change_or_remove_me@example.com",
                                                            target=self.newsletter_targets[0],
                                                            hash_field="hash_to_remove"),
                              NewsletterSubscriptionFactory(email="change_or_remove_me@example.com",
                                                            target=self.newsletter_targets[1],
                                                            hash_field="hash_to_keep"), ]
        self.user = UserFactory(email="change_or_remove_me@example.com")


    def _count_subscriptions(self, email):
        return models.NewsletterSubscription.objects.filter(email=email).count()

    def tearDown(self):
        models.Newsletter.objects.all().delete()
        models.NewsletterSubscription.objects.all().delete()
        models.NewsletterTemplate.objects.all().delete()
        models.NewsletterTarget.objects.all().delete()

    def test_user_changes_email(self):
        """
        Test that, on user email change, also the subscriptions
        to that mail changes accordingly
        """
        self.user.email = "new_email@example.com"
        self.user.save()
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 0)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 2)

    def test_subscription_exists(self):
        """
        Test that subscribe view says "exists" for existing mail in target
        """
        result = self.client.get('/newsletters/subscribe/target-1/change_or_remove_me@example.com/', follow=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {u"result": u"EXISTS"})
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 0)

    def test_subscription_notarget(self):
        """
        Test that subscribe view says "ko" for non existent target
        """
        result = self.client.get('/newsletters/subscribe/not-existent-target/change_or_remove_me@example.com/', follow=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {u"result": u"KO"})
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 0)

    def test_subscription_ok(self):
        """
        Test that subscribe view really subscribes user
        """
        result = self.client.get('/newsletters/subscribe/target-1/new_email@example.com/', follow=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {u"result": u"OK"})
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 1)

    def test_unsubscription_notexists(self):
        """
        Test that unsubscribe view sey "notexists" for non-existing hash
        """
        result = self.client.get('/newsletters/unsubscribe/not_existent_hash/', follow=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {u"result": u"NOTEXISTS"})
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)

    def test_unsubscription_ok(self):
        """
        Test that unsubscribe view really unsubscribes user
        """
        result = self.client.get('/newsletters/unsubscribe/hash_to_remove/', follow=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json.loads(result.content), {u"result": u"OK"})
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 1)
