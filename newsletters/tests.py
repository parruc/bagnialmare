from django.test import TestCase

from factories import NewsletterTemplateFactory
from factories import NewsletterTargetFactory
from factories import NewsletterSubscriptionFactory
from factories import NewsletterFactory
from factories import UserFactory
import models

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
        self.subscriptions = [NewsletterSubscriptionFactory(email="target_1@example.com", target=self.newsletter_targets[0], ),
                              NewsletterSubscriptionFactory(email="target_2@example.com", target=self.newsletter_targets[1], ),
                              NewsletterSubscriptionFactory(email="change_or_remove_me@example.com", target=self.newsletter_targets[0], ),
                              NewsletterSubscriptionFactory(email="change_or_remove_me@example.com", target=self.newsletter_targets[1], ), ]
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
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 0)
        self.user.email = "new_email@example.com"
        self.user.save()
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 0)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 2)

    def test_subscription(self):
        """
        Test that usnubscribe view really unsubscribes user
        """
        self.assertEqual(self._count_subscriptions(email="change_or_remove_me@example.com"), 2)
        self.assertEqual(self._count_subscriptions(email="new_email@example.com"), 0)
        response = self.client.get('/newsletters/unsubscribe/target-1/change_or_remove_me@example.com', follow=True)


