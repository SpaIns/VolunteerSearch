from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Check out homepage
        self.browser.get('http://localhost:8000')

        #Notice to-do in title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #Invited to do to-do right away

        #types "Buy peacock feathers" into text box

        #when hits enter, page updates with 1) buy feathers

        #still text box inviting new items
        #enters "to make a fly"

        #page updates again, now shows both items

        #unique url generated for edith

        #visits url, still shows same stuff

        #done

if __name__ == '__main__':
    unittest.main(warnings='ignore')