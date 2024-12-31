from init_tests import append_to_path
append_to_path()
import unittest
import api_session
from constants import * 


BOLD_NUMBERED_LIST = '''1. **Rules of the Road:** Master traffic laws, signs, and signals.
2. **Vehicle Operation:** Understand how your vehicle works, including basic maintenance.
3. **Safe Driving Practices:** Learn defensive driving techniques and how to handle different road conditions.
4. **Sharing the Road:**  Know how to interact safely with pedestrians, cyclists, and other vehicles.
5. **Driving in Different Conditions:** Practice driving in various weather conditions (rain, fog, etc.) and at night.
6. **Parking Skills:** Be proficient in parallel parking, perpendicular parking, and three-point turns.
7. **Emergency Procedures:** Know what to do in case of an accident or breakdown.
8. **Legal Responsibilities:** Understand your legal obligations as a driver.
9. **Distracted Driving:** Avoid distractions like cell phones and focus on the road.
10. **Practice Regularly:** Consistent practice is key to becoming a safe and confident driver.'''


class TestSession(unittest.TestCase):
    def test_session_client_init(self):
        ''' Test if the attribute client.api matches the expected module. '''
        for client_alias, client_id in ALIAS_TO_CLIENT.items():
            with self.subTest(client_id=client_id):
                session = api_session.Session(client_id)
                
                module_str = str(session.client.api)
                
                # Remove source of import.
                # Example: <module 'x' from '/Library/...
                module_str = module_str.split(' from ')[0]

                if session.type == TYPE_TEST:
                    expected_module_str = 'None'
                elif session.type == TYPE_GEMINI:
                    expected_module_str = "<module 'google.generativeai'"
                elif session.type == TYPE_GOOGLE:
                    expected_module_str = "<module 'googleapi.google'"
                elif session.type == TYPE_OPENAI:
                    expected_module_str = "<module 'openai'"

                self.assertEqual(module_str, expected_module_str)

class TestGeminiFormatResponse(unittest.TestCase):
    ''' Test GeminiClient.format_response(). '''  

    bullet_list = '''
* 1 cup red lentils, rinsed
* 2 cups water or vegetable broth
* 1 tbsp oil
* 1 tsp ground cumin
* 1 tsp ground coriander
* ½ tsp turmeric powder
* ½ tsp garam masala
* ¼ tsp cayenne pepper (optional)
* 1 small onion, chopped
* 2 cloves garlic, minced
* 1 inch ginger, grated
* Salt to taste
* Fresh cilantro, chopped (for garnish)'''
    formatted_bullet_list = '''
\t- 1 cup red lentils, rinsed
\t- 2 cups water or vegetable broth
\t- 1 tbsp oil
\t- 1 tsp ground cumin
\t- 1 tsp ground coriander
\t- ½ tsp turmeric powder
\t- ½ tsp garam masala
\t- ¼ tsp cayenne pepper (optional)
\t- 1 small onion, chopped
\t- 2 cloves garlic, minced
\t- 1 inch ginger, grated
\t- Salt to taste
\t- Fresh cilantro, chopped (for garnish)'''
    bullet_item = '* Large pot or Dutch oven'
    bullet_item_with_asterisk = '\n* Dial *555'
    formatted_bullet_item_with_asterisk = '\n\t- Dial *555'

    @classmethod
    def setUpClass(cls):
        cls.session = api_session.Session(GEMINI_FLASH_ID)
        cls.format_response = cls.session.client.format_response

    @classmethod
    def tearDownClass(cls):
        del cls.session

    def setUp(self):
        self.session.reset()

    def test_bullet_item_with_asterisk(self):
        pre = self.bullet_item_with_asterisk
        expected = self.formatted_bullet_item_with_asterisk

        self.format_response(text=pre)
        post = self.session.client.response

        self.assertEqual(post, expected)
    
    def test_bullet_list(self):
        pre = self.bullet_list
        expected = self.formatted_bullet_list

        self.format_response(text=pre)
        post = self.session.client.response

        self.assertEqual(post, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)