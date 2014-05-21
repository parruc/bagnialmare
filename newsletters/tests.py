from django.test import TestCase

from factories import NewletterTemplateFactory
from factories import NewletterTargetFactory
from factories import NewletterSubscriptionFactory
from factories import NewletterFactory
from factories import NewsletterUserFactory
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
        self.newsletter_template = NewletterTemplateFactory()
        self.newsletter_targets = [NewletterTargetFactory(), NewletterTargetFactory()]
        self.newsletters = [NewletterFactory(target=self.newsletter_target_1),
                            NewletterFactory(target=self.newsletter_target_2), ]
        self.subscriptions = [NewletterSubscriptionFactory(target=self.newsletter_target_1, email="target_1@example.com"),
                              NewletterSubscriptionFactory(target=self.newsletter_target_2, email="target_2@example.com"),
                              NewletterSubscriptionFactory(target=self.newsletter_target_1, email="change_or_remove_me@example.com"),
                              NewletterSubscriptionFactory(target=self.newsletter_target_2, email="change_or_remove_me@example.com"), ]
        self.user = UserFactory(email="change_or_remove_me@example.com")
        self.newsletter_user = NewsletterUserFactory(user=self.user)


    def tearDown(self):
        models.Newsletter.objects.all().delete()
        models.NewsletterSubscription.objects.all().delete()
        models.NewsletterTemplate.objects.all().delete()
        models.NewsletterTarget.objects.all().delete()


    def test_subscription_changed(self):
        """
        Test that, on user email change, also the subscriptions
        to that mail changes accordingly
        """
        self.user.email="new_email@example.com"
        self.user.save()
        old_mail_count = NewletterSubscriptionFactory.objects.filter(email="change_or_remove_me@example.com").count()
        new_mail_count = NewletterSubscriptionFactory.objects.filter(email="new_email@example.com").count()
        self.assertEqual(old_mail_count, 0)
        self.assertEqual(new_mail_count, 2)
