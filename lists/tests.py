#Created 2-6-15 Steffan
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, user_sign_up, organization_sign_up, footer, header, about, register, org_register, job_create, registration_complete, user_profile, org_profile, job_view, update_profile, update_org_profile

#from lists.models import Item, List

# Home page unit tests go here
class AccessibilityTest(TestCase):

    #1
    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    #2
    def test_user_url_resolves_to_user_sign_up(self):
        found = resolve('/usersignup/')
        self.assertEqual(found.func, user_sign_up)
    #3    
    def test_org_url_resolves_to_org_sign_up(self):
        found = resolve('/organizationsignup/')
        self.assertEqual(found.func, organization_sign_up) 
    #4
    def test_footer_url_resolves_to_footer(self):
        found = resolve('/footer/')
        self.assertEqual(found.func, footer)
    #5
    def test_header_url_resolves_to_header(self):
        found = resolve('/header/')
        self.assertEqual(found.func, header)     
    #6
    def test_about_url_resolves_to_about(self):
        found = resolve('/about/')
        self.assertEqual(found.func, about)

    #7
    def test_register_url_resolves_to_user_registration(self):
        found = resolve('/accounts/register/')
        self.assertEqual(found.func, register)

    #8 
    def test_org_register_url_resolves_to_org_registration(self):
        found = resolve('/org/register/')
        self.assertEqual(found.func, org_register)

    #9
    def test_job_creation_url_resolves_to_job_creation(self):
        found = resolve('/org/create/')
        self.assertEqual(found.func, job_create)

    #10
    def test_registration_complete_url_resolves_to_completion(self):
        found = resolve('/accounts/register/complete/')
        self.assertEqual(found.func, registration_complete)

    #11
    def test_user_profile_url_resolves_to_user_profile(self):
        found = resolve('/accounts/profile/')
        self.assertEqual(found.func, user_profile)    

    #12
    def test_org_profile_url_resolves_to_org_profile(self):
        found = resolve('/org/profile/')
        self.assertEqual(found.func, org_profile)

    #13
    def test_job_view_url_resolves_to_job_view(self):
        found = resolve('/jobs/view/')
        self.assertEqual(found.func, job_view)
    
    #14
    def test_update_profile_url_resolves_to_update_profile(self):
        found = resolve('/accounts/update/')
        self.assertEqual(found.func, update_profile)

    #15
    def test_update_org_profile_url_resolves_to_update_org_profile(self):
        found = resolve('/org/update/')
        self.assertEqual(found.func, update_org_profile)

    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
    #    self.assertTrue(response.content.startswith(b'{%'))
    #    self.assertIn(b'<title>Homepage Buttons</title>', response.content)
    #    self.assertTrue(response.content.endswith(b'</html>'))
        

        
#class ModelTest(TestCase):
    
    #tests that models work right go here
        
#Create any other test classes and tests here