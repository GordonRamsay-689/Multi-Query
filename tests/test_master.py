from init_tests import append_to_path
append_to_path()
import unittest
import master
import api_session
import request_handler
from constants import *

class TestMain(unittest.TestCase):
    ''' Tests Master after initialization. '''
    def setUp(self):
        self.master = master.Master()
        self.master.persistent_chat = True
        
        sys_message = None
        aliases =  [TEST_ID]

        self.master.configure(aliases, sys_message)

    # Test functions here

    def test_configure_clients(self):
        # Test during runtime, already tested for startup
        # in TestConfigure.
        pass 

    def tearDown(self):
        del self.master
        
class TestConfigure(unittest.TestCase):
    ''' Tests Master.configure() and relevant helper functions. '''

    def setUp(self):
        self.master = master.Master()

    def tearDown(self):
        del self.master

    def test_configure(self):
        # subtest with different combination of args
        pass # aliases_to_test = [[], []]
        pass # sys_messages_to_test = ['']
        pass # for aliases in aliases_to_test:
        pass #  for sys_message in sys_messages_to_test
        # idk maybe a lot of unnecessary tests this way..

    def test_configure_clients(self):
        pass # probably goes here AND in TestMain.

    def test_populate_clients(self):
        pass

    def test_init_sessions(self):
        pass

class TestParseArgs(unittest.TestCase):
    ''' Test Master.parse_args(). 
    
    e_x = expected_x
    '''

    @classmethod
    def setUpClass(cls):
        # Potentially move inside test_parse_arguments()
        cls.arg_pairs = {
        "no_args": [
                [''], {'query': '',
                'sys_message': None,
                'commands': [], 
                'client_aliases': [] 
                }
            ]
        }

    def test_parse_arguments(self):
        for case, item in self.arg_pairs.items():
            args = item[0]
            expected = item[1]

            with self.subTest(case=case, args=args, expected=expected):
                self.compare(args, expected)

    def compare(self, args, expected):
        query, commands, client_aliases, sys_message = master.parse_arguments(args)

        self.assertEqual(query, expected['query'])
        self.assertEqual(sys_message, expected['sys_message'])
        self.assertCountEqual(commands, expected['commands'])
        self.assertCountEqual(client_aliases, expected['client_aliases'])

    def test_duplicate_args_provided(self):
        pass

    def test_no_sys_message_provided_after(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)