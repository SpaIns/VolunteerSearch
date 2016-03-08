#Created 2-6-15 Steffan
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
        
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_layout_and_styling(self):
        #Lea is a 10 year old who wants to volunteer at a dance organization. 
        #Rea is a volunteer recruiter at the local YNCA.
        #Lea is new in town and doesn't know which organization is looking for volunteers
        #Rea is looking for five volunteers at the day care center. 
        #Lea and Rea hear about VolunteerSearch from two different sources
        #Lea and Rea go to the site
        #Lea and Rea see the home page and ntoicet the banner is nicely centered
        #Lea selects View Positions to learn what her options are    
    
    def test_can_create_a_user_profile(self):
        #Lea finds a position available in her local YNCA and she wants to register
        #Lea goes to the home page
        #Lea sees there is a Volunteer and an Organization button
        #Lea clicks on the Volunteer Button  
        #Lea is taken to another page with a registration form to fill out 
        #Lea fills out her full name
        #Lea fills out her email 
        #Lea fills out her DOB
        #Lea fills out her city 
        #Lea fills out her state 
        #Lea fills out her age 
        #Lea fills out her Bio: her interests, her goals and her experience
        #Lea creates a password
        #Lea re-enters her password
        #Lea enters her skills
        #Lea clicks Register
        
    def test_can_create_an_organization_profile(self):
        #Rea wants to register and post an ad for the new position asap 
        #Rea sees there is a Volunteer and an Organization button
        #Rea clicks on the Organization Button  
        #Rea is taken to another page with a registration form to fill out 
        #Rea fills out her full name
        #Rea fills out the organization's email 
        #Rea fills out the organization's city 
        #Rea fills out the organization's state  
        #Rea fills out a Bio: the organization's environment, the mission statement, types of jobs avail
        #Rea creates a password
        #Rea re-enters her password
        #Rea clicks Register