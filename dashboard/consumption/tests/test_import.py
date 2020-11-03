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
        print(self.USER_FILE_DIR)
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
