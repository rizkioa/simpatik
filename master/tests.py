from django.test import TestCase

# Create your tests here.
var = "9471020"
var2 = "9471020014"

print var[0:2]
print var[2:4]
print var[4:]
print var2[7:]

import urllib

url = "%7B%22mesin_huller%22:%22Mesin%20Bensin%22,%20%22model_type%22:%20%22assafdf%22%7D"
url = urllib.unquote(url).decode('utf8') 
print url