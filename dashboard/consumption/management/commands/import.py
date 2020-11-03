import csv
import sys
from datetime import datetime as dt
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from dashboard import settings
from consumption.models import User, Consumption


class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        parser.add_argument('user_data_path',
                            nargs='?',
                            default=settings.USER_FILE_DEFAULT,
                            help='path to user data \'file\'')
        parser.add_argument('consumption_folder_path',
                            nargs='?',
                            default=settings.CONSUMPTION_FOLDER_DEFAULT,
                            help='path to consumption data \'folder\'')

    def handle(self, *args, **options):
        """import data"""

        self.import_user_data(options['user_data_path'])
        self.import_consumption_data(options['consumption_folder_path'])

    def import_user_data(self, file_path):
        try:
            file = open(file_path, newline='\n')

        except IOError:
            sys.stdout.write(f'File does not exist : {file_path}\n')
            sys.exit(1)

        else:
            reader = csv.reader(file)
            # skip header
            header = next(reader)

            users = []

            # read rows and insert user data
            for row in reader:
                user = User(id=row[0], area=row[1], tariff=row[2])
                users.append(user)

            # insert user data
            User.objects.bulk_create(users, ignore_conflicts=True)

    def import_consumption_data(self, folder_path):
        consumption_list = []

        for user in User.objects.all():
            try:
                file = open(f'{folder_path}/{user.id}.csv', newline='\n')
            except IOError:
                sys.stdout.write('File does not exist or cannot open : '
                                 f'{user.id}.csv\n')
                continue

            reader = csv.reader(file)
            # skip header
            header = next(reader)

            sys.stdout.write(f'\rImporting {user.id}.csv...')
            sys.stdout.flush()

            # read rows and add list
            for row in reader:
                aware_time = make_aware(dt.strptime(row[0],
                                        '%Y-%m-%d %H:%M:%S'))
                consumption = Consumption(user=user,
                                          datetime=aware_time,
                                          consumption=row[1])
                consumption_list.append(consumption)

        # insert consumption data
        Consumption.objects.bulk_create(consumption_list)

        sys.stdout.write('\nComplete!\n')
