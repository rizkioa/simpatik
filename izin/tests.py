from django.test import TestCase

# Create your tests here.

import datetime

now = datetime.datetime.now()
print now.strftime("%f")[:4]
print now.strftime("%Y")
print now.strftime("%d")
print now.strftime("%m")
print now.strftime("%S")


