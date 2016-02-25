#Created 2-6-15 Steffan
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

from lists.models import Item, List

class HomePageTest(TestCase):
    
    #home page unit tests go here
	def test_url_resolves_to_home_page(self):
		pass
        
class ModelTest(TestCase):
    
    #tests that models work right go here
        
#Create any other test classes and tests here