import string
import random

import factory
from factory import fuzzy
from django.contrib.gis.geos import Point
from bagni import search
from bagni import models as bagni_models
from django.contrib.auth import models as auth_models
from authauth import models as authauth_models

DEFAULT_PASSWORD = "password"

class BagnoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Bagno'
    name = factory.Sequence(lambda n: "bagno%03d" % n)
    mail = factory.LazyAttribute(lambda o: o.name + "@example.com")
    number = fuzzy.FuzzyText(length=3, chars=string.digits)
    point = factory.LazyAttribute(lambda o: Point(
        [50+random.random()*10, 30+random.random()*10])
        )
    description = fuzzy.FuzzyText(length=50)

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'auth.User'
    username = factory.Sequence(lambda n: "user%03d" % n)
    email = factory.LazyAttribute(lambda o: o.username + "@example.com")
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

def tearDownTestFactory():
    search.delete_index()
    bagni_models.Bagno.objects.all().delete()
    bagni_models.Service.objects.all().delete()
    bagni_models.ServiceCategory.objects.all().delete()
    bagni_models.District.objects.all().delete()
    bagni_models.Municipality.objects.all().delete()
    bagni_models.Language.objects.all().delete()
    auth_models.User.objects.all().delete()
    authauth_models.objects.all().delete()

def setUpTestFactory(test_dimension=10):
    """
    create structured data from factories for running tests
    @param test_dimension: how many Bagno objects are created
    """
    search.recreate_index()
    districts = []
    for i in range(2):
        districts.append(DistrictFactory())
    municipalities = []
    for i in range(test_dimension):
        municipalities.append(MunicipalityFactory(district = districts[i%2]))
    service_categories = []
    for i in range(3):
        service_categories.append(ServiceCategoryFactory())
    services = []
    for i in range(test_dimension * 2):
        services.append(ServiceFactory(category = service_categories[i%3]))
    bagni = []
    for i in range(test_dimension):
        bagno = BagnoFactory()
        bagno.municipality = municipalities[i]
        bagno.services = random.sample(services, 4)
        bagni.append(bagno)
        bagno.save()
    normal_user = UserFactory()
    manager = ManagerFactory(bagni = [random.choice(bagni)])
    return dict(
            districts = districts,
            municipalities = municipalities,
            service_categories = service_categories,
            services = services,
            bagni = bagni,
            normal_user = normal_user,
            manager = manager,
            )



