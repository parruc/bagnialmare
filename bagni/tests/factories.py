import factory
from factory import fuzzy
#import bagni
from django.contrib import auth
#import authauth
from django.contrib.gis.geos import Point

DEFAULT_PASSWORD = "password"

class BagnoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = 'bagni.Bagno'
    name = factory.Sequence(lambda n: "bagno%03d" % n)
    mail = factory.Sequence(lambda n: "bagno%03d@example.com" % n)
    number = factory.Sequence(lambda n: "%03d" % n)
    point = factory.Sequence(lambda n: Point([40.0 + n, 50.0 + n]))
    description = fuzzy.FuzzyText(length=50)

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = auth.models.User
    username = factory.Sequence(lambda n: "user%03d" % n)
    email = factory.Sequence(lambda n: "user%03d@example.com" % n)
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

