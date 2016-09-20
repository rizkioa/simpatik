from django.test import TestCase

# Create your tests here.

action_names = {
    '1': 'Addition',
    2: 'Deletion',
    3: 'Change',
}

print action_names[2]

import datetime
from dateutil.relativedelta import relativedelta
now = datetime.datetime.now()
tgl = datetime.date(now.year, now.month+3, 1)
print tgl-relativedelta(months=1)
