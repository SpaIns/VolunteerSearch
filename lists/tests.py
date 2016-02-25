#Created 2-6-15 Steffan
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, user_sign_up, organization_sign_up

#from lists.models import Item, List

class AccessibilityTest(TestCase):
    
    #home page unit tests go here
	def test_root_url_resolves_to_home_page(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>Homepage Buttons</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
		
	def test_user_url_resolves_to_user_sign_up(self):
		found = resolve('/usersignup/')
		self.assertEqual(found.func, user_sign_up)
		
	def test_org_url_resolves_to_org_sign_up(self):
		pass
        
#class ModelTest(TestCase):
    
    #tests that models work right go here
        
#Create any other test classes and tests here