import pathlib
from dashboard.settings import * # noqa


USER_FILE_DEFAULT = str(pathlib.Path('__file__')) + \
                    '/consumption/tests/data/user_data.csv'
CONSUMPTION_FILE_DEFAULT = str(pathlib.Path('__file__')) + \
                           '/consumption/tests/data/consumption'
