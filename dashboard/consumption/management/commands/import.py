import sys
from datetime import datetime as dt
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
from dashboard import settings
from consumption.models import User, Consumption
import pandas as pd


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
            sys.stdout.write(f'Start importing user data...')
            chunked_df = pd.read_csv(file_path, header=0, chunksize=100)
            df = pd.concat((r for r in chunked_df), ignore_index=True)

        except IOError:
            sys.stdout.write(f'File does not exist : {file_path}\n')
            sys.exit(1)

        else:
            users = []
            
            # read rows and insert user data
            for row in df.itertuples():
                user = User(id=row[1], area=row[2], tariff=row[3])
                users.append(user)
            User.objects.bulk_create(users, ignore_conflicts=True)
            sys.stdout.write('\nComplete importing user data!\n')

    def import_consumption_data(self, folder_path):
        consumption_list = []
        sys.stdout.write(f'Start importing consumption data...\n')
        for user in User.objects.all():
            try:
                chunked_df = pd.read_csv(f'{folder_path}/{user.id}.csv', header=0, chunksize=100)
                df = pd.concat((r for r in chunked_df), ignore_index=True)

            except IOError:
                sys.stdout.write('File does not exist or cannot open : '
                                 f'{user.id}.csv\n')
                continue

            sys.stdout.write(f'\rImporting {user.id}.csv...')
            sys.stdout.flush()

            # read rows and add list
            for row in df.itertuples():
                aware_time = make_aware(dt.strptime(row[1],
                                        '%Y-%m-%d %H:%M:%S'))
                consumption = Consumption(user=user,
                                          datetime=aware_time,
                                          consumption=row[2])
                consumption_list.append(consumption)

        # insert consumption data
        Consumption.objects.bulk_create(consumption_list, ignore_conflicts=True)

        sys.stdout.write('\nComplete!\n')
