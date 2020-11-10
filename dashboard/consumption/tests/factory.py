import factory
from django.utils import timezone
from consumption import models


class ConsumptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Consumption

    datetime = timezone.now()
    consumption = 10.0


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    id = 1
    area = 'a1'
    tariff = 't1'
    consumption = factory.RelatedFactory(ConsumptionFactory, 'user')