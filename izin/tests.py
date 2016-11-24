from django.test import TestCase

# Create your tests here.

# import datetime

# now = datetime.datetime.now()
# print now.strftime("%f")[:4]
# print now.strftime("%Y")
# print now.strftime("%d")
# print now.strftime("%m")
# print now.strftime("%S")


# print '{:,.2f}'.format(18446744073709551616)

from htmlvalidator.client import ValidatingClient

class CheckExample(TestCase):
	def setUp(self):
	self.client = ValidatingClient()

def tearDown(self):
	pass

def test_example(self):
	response = self.client.get('/example/')
	self.assertEqual(response.status_code, 200)