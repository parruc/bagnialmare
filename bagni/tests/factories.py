import string
from random import random

import factory
from factory import fuzzy
from django.contrib import auth
from django.contrib.gis.geos import Point

DEFAULT_PASSWORD = "password"

class BagnoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Bagno'
    name = factory.Sequence(lambda n: "bagno%03d" % n)
    mail = factory.LazyAttribute(lamda o: o.name + "@example.com")
    number = fuzzy.FuzzyText(lenght=3, chars=string.digits)
    point = factory.LazyAttribute(lambda o: Point([50+random()*10, 30+random()*10]))
    description = fuzzy.FuzzyText(length=50)

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = auth.models.User
    username = factory.Sequence(lambda n: "user%03d" % n)
    email = factory.LazyAttribute(lamda o: o.username + "@example.com")
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)

class ManagerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'authauth.Manager'
    user = factory.SubFactory(UserFactory)
    privacy = True

    @factory.post_generation
    def bagni(self, create, bagni, **kwargs):
        if not create:
            return
        if bagni:
            for bagno in bagni:
                self.bagni.add(bagno)

class DistrictFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.District'
    name = factory.Sequence(lambda n: "district%03d" % n)
    description = fuzzy.FuzzyText(length=50)

class MunicipalityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Municipality'
    name = factory.Sequence(lambda n: "municipality%03d" % n)
    description = fuzzy.FuzzyText(length=50)
    district = factory.SubFactory(DistrictFactory)

class LanguageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Language'
    name = factory.Iterator(['en', 'fr', 'es', 'it', 'de'])
    description = fuzzy.FuzzyText(length=50)

class ServiceCategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.ServiceCategory'
    name = factory.Sequence(lambda n: "service_category%03d" % n)
    description = fuzzy.FuzzyText(length=200)

class ServiceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Service'
    name = factory.Sequence(lambda n: "service%03d" % n)
    description = fuzzy.FuzzyText(length=200)
    category = factory.SubFactory(ServiceCategoryFactory)
    free = fuzzy.FuzzyChoice([True, False])
