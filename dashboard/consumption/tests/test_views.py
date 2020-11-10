from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Consumption
from .factory import UserFactory


class TestSummaryView(TestCase):
    """Test SummaryView"""

    def setUp(self):
        # create user and consumption data
        super().setUp()
        self.user1 = UserFactory()
        self.user2 = UserFactory(id=2,
                                 area='a2',
                                 tariff="t2",
                                 consumption__consumption=20.0)

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


class TestDetailView(TestCase):
    """Test DetailView"""

    def setUp(self):
        # create user and consumption data
        super().setUp()
        self.user1 = UserFactory()
        self.user2 = UserFactory(id=2,
                                 area='a2',
                                 tariff="t2",
                                 consumption__consumption=20.0)

    def test_get_detail(self):
        response = self.client.get(reverse('consumption:detail',
                                           kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].id, 1)
        self.assertEqual(response.context['object'].area, 'a1')
        self.assertEqual(response.context['object'].tariff, 't1')

    def test_get_queryset(self):
        response = self.client.get(reverse('consumption:detail',
                                           kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['consumption_count'], 1)

    def test_empty_user_data(self):
        response = self.client.get(reverse('consumption:detail',
                                           kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)
