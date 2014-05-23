#import string
from random import randrange
import factory
from factory.fuzzy import FuzzyText

from django.contrib.webdesign import lorem_ipsum
from django.contrib.auth import models as auth_models

from newsletters import models as newsletters_models


DEFAULT_PASSWORD = "password"
def random_email():
    return "@".join(lorem_ipsum.words(2)) + ".com"

class NewsletterTemplateFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = newsletters_models.NewsletterTemplate
    FACTORY_FOR = newsletters_models.NewsletterTemplate
    name = FuzzyText(prefix="newsletter template ", length=15)
    path = "newsletters/staff_template.html"


class NewsletterTargetFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = newsletters_models.NewsletterTarget
    FACTORY_FOR = newsletters_models.NewsletterTarget
    name = FuzzyText(prefix="newsletter target ", length=15)


class NewsletterFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = newsletters_models.Newsletter
    FACTORY_FOR = newsletters_models.Newsletter
    name = FuzzyText(prefix="newsletter ", length=15)
    subject = lorem_ipsum.words(randrange(1, 3))
    text = lorem_ipsum.paragraphs(randrange(1, 10))
    sent_to = None
    sent_on = None
    target = factory.SubFactory(NewsletterTargetFactory)
    template = factory.SubFactory(NewsletterTemplateFactory)


class NewsletterSubscriptionFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = newsletters_models.NewsletterSubscription
    FACTORY_FOR = newsletters_models.NewsletterSubscription
    email = random_email()
    target = factory.SubFactory(NewsletterTargetFactory)
    hash_field = "hash"


class NewsletterUserFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = newsletters_models.NewsletterUser
    FACTORY_FOR = newsletters_models.NewsletterUser
    user = factory.SubFactory(auth_models.User)
    old_email = random_email()


class UserFactory(factory.DjangoModelFactory):
    #class Meta:
    #    model = auth_models.User
    FACTORY_FOR = auth_models.User
    username = FuzzyText(prefix="user_", length=5)
    email = random_email()
    password = DEFAULT_PASSWORD
