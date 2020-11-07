from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Consumption


class TestSummaryView(TestCase):
    """Test SummaryView"""

    def setUp(self):
        # create user and consumption data
        super().setUp()
        self.user1 = User.objects.create(id=1, area='a1', tariff='t1')
        self.user2 = User.objects.create(id=2, area='a2', tariff='t2')
        self.consumption = Consumption.objects.create(id=1,
                                                      user=self.user1,
                                                      datetime=timezone.now(),
                                                      consumption=10.0)
        self.consumption = Consumption.objects.create(id=2,
                                                      user=self.user2,
                                                      datetime=timezone.now(),
                                                      consumption=20.0)

    def test_get_user(self):
        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_list']), 2)

    def test_get_queryset(self):
        response = self.client.get(reverse('consumption:summary'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['consumption_count'], 2)

    def test_no_user_data(self):
        User.objects.all().delete()
        # check the number of user
        self.assertEqual(User.objects.all().count(), 0)

        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['user_list']), 0)
