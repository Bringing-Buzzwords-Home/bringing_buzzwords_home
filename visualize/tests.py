from django.test import TestCase
from .models import County, State, GuardianCounted, Item, Crime, State
# Create your tests here.

class CountyTestCase(TestCase):
    def setup(self):
        County.objects.create()
