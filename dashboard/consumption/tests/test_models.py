from django.utils import timezone
from django.test import TestCase, Client
from ..models import User, Consumption


class TestUserModel(TestCase):
    """Test UserModel"""

    def test_empty_user_data(self):
        user = User.objects.all()
        self.assertEqual(user.count(), 0)

    def test_create_user(self):
        user = User.objects.create(id=1, area='a1', tariff='t2')

        new_user = User.objects.all()
        self.assertEqual(len(new_user), 1)
        self.assertEqual(user.id, new_user[0].id)
        self.assertEqual(user.area, new_user[0].area)
        self.assertEqual(user.tariff, new_user[0].tariff)
        self.assertEqual(str(user.id), str(new_user[0]))

    def test_update_user(self):
        user = User.objects.create(id=1, area='a1', tariff='t2')
        # update user
        user.area = 'a2'
        user.tariff = 't2'
        user.save()

        new_user = User.objects.all()
        self.assertEqual(len(new_user), 1)
        self.assertEqual(new_user[0].id, 1)
        self.assertEqual(new_user[0].area, 'a2')
        self.assertEqual(new_user[0].tariff, 't2')

    def test_delete_user(self):
        User.objects.create(id=1, area='a1', tariff='t2')
        self.assertEqual(User.objects.all().count(), 1)
        # delete all users
        User.objects.all().delete()

        self.assertEqual(User.objects.all().count(), 0)


class TestConsumptionModel(TestCase):
    """Test ConsumptionModel"""

    def setUp(self):
        # create user data
        super().setUp()
        self.user = User.objects.create(id=1, area='a1', tariff='t1')

    def test_empty_user_data(self):
        consumption = Consumption.objects.all()
        self.assertEqual(consumption.count(), 0)

    def test_create_consumption(self):
        consumption = Consumption.objects.create(id=1,
                                                 user=self.user,
                                                 datetime=timezone.now(),
                                                 consumption=10.0)

        new_consumption = Consumption.objects.all()

        self.assertEqual(len(new_consumption), 1)
        self.assertEqual(consumption.id, new_consumption[0].id)
        self.assertEqual(consumption.user, new_consumption[0].user)
        self.assertEqual(consumption.datetime, new_consumption[0].datetime)
        self.assertEqual(consumption.consumption, new_consumption[0].consumption)
        self.assertEqual(str(consumption.id), str(new_consumption[0]))

    def test_update_consumption(self):
        consumption = Consumption.objects.create(id=1,
                                                 user=self.user,
                                                 datetime=timezone.now(),
                                                 consumption=10.0)
        # update consumption
        consumption.consumption = 20.0
        consumption.save()

        new_consumption = Consumption.objects.all()
        self.assertEqual(len(new_consumption), 1)
        self.assertEqual(new_consumption[0].id, 1)
        self.assertEqual(new_consumption[0].consumption, 20.0)

    def test_delete_consumption(self):
        Consumption.objects.create(id=1,
                                   user=self.user,
                                   datetime=timezone.now(),
                                   consumption=10.0)
        self.assertEqual(Consumption.objects.all().count(), 1)
        # delete all coonsumption
        Consumption.objects.all().delete()

        self.assertEqual(Consumption.objects.all().count(), 0)
