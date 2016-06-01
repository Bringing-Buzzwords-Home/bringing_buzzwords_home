from .models import GuardianDeaths
import csv
import datetime

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
          'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}


def handle_guardian_counted_csv(csv_path):
    with open(csv_path) as f:
        counted_reader = csv.DictReader(f)
        for row in counted_reader:
            try:
                victim_age = int(row['age'])
            except ValueError:
                victim_age = None
            counted = GuardianDeaths(name=row['name'],
                                     age=victim_age,
                                     gender=row['gender'],
                                     race_ethnicity=row['raceethnicity'],
                                     date=datetime.date(
                                        year=int(row['year']),
                                        month=months[row['month']],
                                        day=int(row['day'])),
                                     street_address=row['streetaddress'],
                                     city=row['city'],
                                     state=row['state'],
                                     classification=row['classification'],
                                     law_enforcement_agency=row['lawenforcementagency'],
                                     armed=row['armed'])
            counted.save()
