import pathlib
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from consumption.models import User, Consumption
from dashboard.settings import BASE_DIR


class TestImport(TestCase):
    def setUp(self):
        super().setUp()
        self.USER_FILE_DIR = f'{pathlib.Path(__file__).parent}'\
                             '/data/user_data.csv'
        self.CONSUMPTION_FOLDER_DIR = f'{pathlib.Path(__file__).parent}'\
                                      '/data/consumption'

    def test_command(self):
        out = StringIO()
        call_command('import',
                     self.USER_FILE_DIR,
                     self.CONSUMPTION_FOLDER_DIR,
                     stdout=out)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(Consumption.objects.all().count(), 9)

    def test_wrong_file_path(self):
        out = StringIO()
        try:
            call_command('import',
                         './test/test.csv',
                         self.CONSUMPTION_FOLDER_DIR,
                         stdout=out,
                         stderr=StringIO())
        except SystemExit:
            self.assertEqual(User.objects.all().count(), 0)
            self.assertEqual(Consumption.objects.all().count(), 0)

    def test_wrong_folder_path(self):
        out = StringIO()

        call_command('import',
                     self.USER_FILE_DIR,
                     './testdir',
                     stdout=out,
                     stderr=StringIO())
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(Consumption.objects.all().count(), 0)

    def test_duplicate_user(self):
        out = StringIO()

        user1 = User.objects.create(id=1, area='AA', tariff='BB')
        user2 = User.objects.create(id=2, area='CC', tariff='DD')

        call_command('import',
                     self.USER_FILE_DIR,
                     self.CONSUMPTION_FOLDER_DIR,
                     stdout=out,
                     stderr=StringIO())

        # check unupdated user data
        new_user = User.objects.all().order_by('id')
        self.assertEqual(new_user.count(), 2)
        self.assertEqual(new_user[0].id, user1.id)
        self.assertEqual(new_user[0].area, user1.area)
        self.assertEqual(new_user[0].tariff, user1.tariff)

        self.assertEqual(new_user[1].id, user2.id)
        self.assertEqual(new_user[1].area, user2.area)
        self.assertEqual(new_user[1].tariff, user2.tariff)

        self.assertEqual(Consumption.objects.all().count(), 9)
