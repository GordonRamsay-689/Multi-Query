from init_tests import append_to_path
append_to_path()
import unittest
import api_session
from constants import * 

BULLET_ITEM = '* Large pot or Dutch oven'
BULLET_ITEM_WITH_ASTERISK = '\n* Dial *555'
FORMATTED_BULLET_ITEM_WITH_ASTERISK = '\n\t- Dial *555'

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

BULLET_LIST = '''
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
FORMATTED_BULLET_LIST = '''
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

RECIPE = '''**Yields:** 4 servings
**Prep time:** 10 minutes
**Cook time:** 30 minutes 

**Ingredients:**
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
* Fresh cilantro, chopped (for garnish)

**Equipment:**
* Large pot or Dutch oven

**Instructions**

**Get started:**
1. Rinse the red lentils under cold water until the water runs clear.

**Cook the daal:**
1. Heat the oil in a large pot or Dutch oven over medium heat. Add the onion and cook until softened, about 5 minutes. 
2. Add the garlic and ginger and cook for another minute until fragrant.
3. Stir in the cumin, coriander, turmeric, garam masala, and cayenne pepper (if using) and cook for 30 seconds, or until fragrant.
4. Add the rinsed red lentils and water or broth to the pot. Bring to a boil, then reduce heat to low, cover, and simmer for 20-25 minutes, or until the lentils are tender and have broken down.
5. Stir occasionally to prevent sticking. If the daal becomes too thick, add more water or broth as needed.

**Finish and serve:**
1. Season with salt to taste.
2. Garnish with fresh cilantro and serve hot with rice, naan, or roti.'''

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
        pre = BULLET_ITEM_WITH_ASTERISK
        expected = FORMATTED_BULLET_ITEM_WITH_ASTERISK

        self.format_response(text=pre)
        post = self.session.client.response

        self.assertEqual(post, expected)
    
    def test_bullet_list(self):
        pre = BULLET_LIST
        expected = FORMATTED_BULLET_LIST

        self.format_response(text=pre)
        post = self.session.client.response

        self.assertEqual(post, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)