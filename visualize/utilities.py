from .models import GuardianDeaths
import csv
import datetime

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}


def handle_guardian_counted_csv(csv_path):
    with open(csv_path) as f:
        counted_reader = csv.DictReader(f)
        counted = GuardianDeaths(name=counted_reader['name'],
                                 age=int(counted_reader['age']),
                                 gender=counted_reader['gender'],
                                 race_ethnicity=counted_reader['raceethnicity'],
                                 date=datetime.date(
                                    year=int(counted_reader['year']),
                                    month=months[counted_reader['month']],
                                    day=int(counted_reader['day'])),
                                 street_address=counted_reader['streetaddress'],
                                 )
