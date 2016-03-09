#Created 2-6-15 Steffan
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import time

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
        
    #def check_for_row_in_list_table(self, row_text):
    #    table = self.browser.find_element_by_id('id_list_table')
    #    rows = table.find_elements_by_tag_name('tr')
    #    self.assertIn(row_text, [row.text for row in rows])
    
    def test_can_create_a_user_profile(self):
        #Lea finds a position available in her local YNCA and she wants to register
        #Lea goes to the home page
        self.browser.get(self.server_url)
        #Lea sees there is a Volunteer and an Organization button
        #Lea clicks on the Volunteer Button  
        volunteerButton = self.browser.find_element_by_class_name('VolunteerHomeButton')
        volunteerButton.click()
        self.browser.implicitly_wait(10)
        #Lea is taken to another page with a registration form to fill out 
        #Lea fills out her full name
        name_fill = self.browser.find_element_by_id('id_user_name')
        name_fill.send_keys('Lea')
        #Lea fills out her email 
        email_fill = self.browser.find_element_by_id('id_email')
        email_fill.send_keys('lea@gmailfake.com')
        #Lea fills out her DOB
            #we're pretending she was born 1-1-1920
        #Lea fills out her city 
        city_fill = self.browser.find_element_by_id('id_location_city')
        city_fill.send_keys('Seattle')
        #Lea fills out her state 
            #left as default WA
        #Lea fills out her age 
        age_select = Select(self.browser.find_element_by_id('id_age'))
        age_select.select_by_visible_text('65+')
        
        self.browser.implicitly_wait(10)
        #Lea fills out her Bio: her interests, her goals and her experience
        bio_fill = self.browser.find_element_by_id('id_bio')
        bio_fill.send_keys('Im Lea and I like to volunteer, especially as a tester')
        #Lea creates a password
        pass_fill = self.browser.find_element_by_id('id_password1')
        pass_fill.send_keys('badpassword')
        #Lea re-enters her password
        pass_repeat_fill = self.browser.find_element_by_id('id_password2')
        pass_repeat_fill.send_keys('badpassword')
        
        #skills do not show up for whatever reason....
        #Lea enters her skills
        #skill_select = self.browser.find_element_by_id('id_skills_0')
        #skill_select.click()
        #Lea clicks Register
        register_button = self.browser.find_element_by_xpath("//*[@type='submit']")
        register_button.click()
        self.browser.implicitly_wait(10)
        
    def test_can_create_an_organization_profile(self):
        #pass
        #Rea wants to register and post an ad for the new position asap 
        #Rea sees there is a Volunteer and an Organization button
        self.browser.get(self.server_url)
        #Rea clicks on the Organization Button
        organizationButton = self.browser.find_element_by_class_name('OrganizationHomeButton')
        organizationButton.click()
        self.browser.implicitly_wait(10)
        #Rea is taken to another page with a registration form to fill out 
        #Rea fills out her full name
        name_fill = self.browser.find_element_by_id('id_user_name')
        name_fill.send_keys('Rea')
        #Rea fills out the organization's email 
        email_fill = self.browser.find_element_by_id('id_email')
        email_fill.send_keys('rea@gmailfake.com')
        #Rea fills out the organization's city 
        city_fill = self.browser.find_element_by_id('id_location_city')
        city_fill.send_keys('Seattle')
        #Rea fills out the organization's state 
            #left as default WA
        #Rea fills out a Bio: the organization's environment, the mission statement, types of jobs avail
        bio_fill = self.browser.find_element_by_id('id_bio')
        bio_fill.send_keys('Im Rea with ReaOrg, a company that loves to test!')
        #Rea creates a password
        pass_fill = self.browser.find_element_by_id('id_password1')
        pass_fill.send_keys('badpassword')
        #Rea re-enters her password
        pass_repeat_fill = self.browser.find_element_by_id('id_password2')
        pass_repeat_fill.send_keys('badpassword')
        #Rea clicks Register
        register_button = self.browser.find_element_by_xpath("//*[@type='submit']")
        register_button.click()
        self.browser.implicitly_wait(10)
        
    #def test_organization_can_create_a_job(self):
    #    pass
        
        
    def test_layout_and_styling(self):
        #Lea is a 10 year old who wants to volunteer at a dance organization. 
        #Rea is a volunteer recruiter at the local YNCA.
        #Lea is new in town and doesn't know which organization is looking for volunteers
        #Rea is looking for five volunteers at the day care center. 
        #Lea and Rea hear about VolunteerSearch from two different sources
        #Lea and Rea go to the site
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        #Lea and Rea see the home page and noticed the carasol is nicely centered
        carasol = self.browser.find_element_by_class_name('carousel-caption')
        self.assertAlmostEqual(carasol.location['x'] + carasol.size['width'] /2,
            512,
            delta=15
        )