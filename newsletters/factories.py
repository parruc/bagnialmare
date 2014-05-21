#import string
from random import randrange
from uuid import uuid4
import factory

from django.contrib.webdesign import lorem_ipsum


DEFAULT_PASSWORD = "password"
def random_email():
    return lorem_ipsum.words(1) + "@" + lorem_ipsum.words(1) + ".com"

class NewletterTemplateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'newsletters.NewletterTemplate'
    name = factory.fuzzy.FuzzyText(prefix="newsletter template ", length=15)
    path = "newsletters/staff_template.html"


class NewletterTargetFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'newsletters.NewletterTarget'
    name = factory.fuzzy.FuzzyText(prefix="newsletter target ", length=15)


class NewsletterFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'newsletters.Newsletter'
    name = factory.fuzzy.FuzzyText(prefix="newsletter ", length=15)
    subject = lorem_ipsum.words(randrange(1, 3))
    text = lorem_ipsum.paragraphs(randrange(1, 10))
    sent_to = None
    sent_on = None
    target = factory.SubFactory(NewletterTargetFactory)
    template = factory.SubFactory(NewletterTemplateFactory)


class NewletterSubscriptionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'newsletters.NewletterSubscription'
    email = random_email()
    target = factory.SubFactory(NewletterTargetFactory)
    hash_field = uuid4().hex


class UserFactory():
    FACTORY_FOR = 'django.contrib.auth.models.User'
    first_name = lorem_ipsum.words(1)
    last_name = lorem_ipsum.words(1)
    admin = False
    email = random_email()
    password = DEFAULT_PASSWORD

class NewsletterUserFactory():
    user = factory.SubFactory(NewletterTargetFactory)
    old_email = random_email()
