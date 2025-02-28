from init_tests import append_to_path
append_to_path()

import unittest
from unittest.mock import patch

import io
import sys

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

    @patch('master.google_generativeai_imported', False)
    def test_configure_clients_google_generativeai_not_imported(self):
        self.master.clients = [GEMINI_FLASH_ID]

        self.master.configure_clients()
        self.assertCountEqual([], self.master.clients)
        self.assertEqual(False, self.master.configured_gemini)

    @patch('master.openai_imported', False)
    def test_configure_clients_openai_not_imported(self):
        self.master.clients = [GPT_4O_MINI_ID, DEEPSEEK_R1_FREE]

        self.master.configure_clients()
        self.assertCountEqual([], self.master.clients)
        self.assertEqual(False, self.master.configured_openai)
        self.assertEqual(False, self.master.configured_deepseek)
        
    def test_configure_clients_no_api_key_google_generativeai(self):
        pass

    def test_populate_clients(self):
        with self.subTest(n=0, aliases=[]):
            self.master.populate_clients([])
            self.assertCountEqual([], self.master.clients)

        for n in [1, 2, 3]:
            aliases_to_test = list(ALIAS_TO_CLIENT.keys())
            while aliases_to_test:
                self.master.clients = []
                aliases = []

                for i in range(n):
                    if aliases_to_test:
                        alias = aliases_to_test.pop()
                        aliases.append(alias)
                    else:
                        break

                client_id = ALIAS_TO_CLIENT[alias]
                client_type = CLIENT_ID_TO_TYPE[client_id]
                if client_type == TYPE_GOOGLE:
                    continue

                expected = set()
                for alias in aliases:
                    expected.add(ALIAS_TO_CLIENT[alias])

                with self.subTest(n=n, aliaess=aliases):
                    self.master.populate_clients(aliases)
                    self.assertCountEqual(expected, self.master.clients)
        
    def test_init_sessions_stream_enabled_active_stream(self):
        ''' Tests Master.init_session() toggling of client.stream_enabled 
        when Master.active_stream is either True of False.
        
        Only one stream can be active at a time. '''
        
        self.master.stream_enabled = True

        for state in [True, False]:
            self.master.active_stream = state
            self.master.sessions = []
            self.master.clients = [GEMINI_FLASH_ID, GPT_4_ID]

            with self.subTest(active_stream=state):
                self.master.init_sessions(sys_message=None)
                
                states = []
                for session in self.master.sessions:
                    states.append(session.client.stream_enabled)

                expected = [False, False] if state == True else [True, False]

                self.assertCountEqual(expected, states)

class TestParseArgs(unittest.TestCase):
    ''' Test Master.parse_args(). 
    
    Each item (list) in self.arg_pairs dict contains a
    dict of ArgPair().arg_pair consisting of a list of 
    arguments (equivalent to sys.argv[1:]) and a dict 
    containing the expected values for each value returned
    by Master.parse_arguments().

    The list is passed to Master.parse_arguments() and 
    the return values are compared to the expected values.

    Keys for cases in self.arg_pairs are the arguments
    passed in order, abbreviated:

    'q': 'query'
    's': 'sys_message'
    'c': 'command'
    'a': 'client_aliases'

    Unless cases are more specific and manually created.
    '''

    def setUp_test_general_combinations(self):
        self.key_components = ['q', 'a', 'c', 's']

        self.keys = []

        self.generate_keys('', 0, len(self.key_components))

        self.arg_pairs = {}

        self.generate_arg_pairs()

    def generate_keys(self, key, depth, max_depth): 
        if depth == max_depth:
            return

        for i in range(max_depth):
            char = self.key_components[i]

            if key and char == 'q':
                continue

            if char in key:
                if char == 'c' or char == 'a':
                    pass # Allow multiple aliases, commands
                else:
                    continue

            new_key = key + char
            self.keys.append(new_key)

            self.generate_keys(new_key, depth + 1, max_depth)

    def generate_arg_pairs(self):
        for key in self.keys:
            pair = ArgPair().arg_pair

            aliases = list(ALIAS_TO_CLIENT.keys())

            commands = VALID_COMMANDS.copy()
            commands.remove(SYS_COMMAND) # Manually added later

            args = []
            expected = pair[1]

            if key.startswith('q'):
                args.append("text")
                expected["query"] = "text"
            if 'a' in key:
                alias = aliases.pop()

                args.append(alias)
                expected["client_aliases"].append(alias)
            if 'c' in key:
                command = commands.pop()

                args.append(command)
                expected["commands"].append(command)
            if 's' in key:
                args.append(SYS_COMMAND)
                args.append("msg")
                expected["sys_message"] = "msg"
            
            pair[0] = args

            self.arg_pairs[key] = pair

    @patch("sys.stdout", new_callable=io.StringIO)
    def compare_fatal_error_output(self, args, unformatted_e_out, mock_stdout):        
        try:
            master.parse_arguments(args)
        except SystemExit:
            pass
        
        expected = f"\x1b[38;5;1mError: \x1b[0m\t{unformatted_e_out}\x1b[0m\n"
        self.assertEqual(mock_stdout.getvalue(), expected)

    def compare(self, args, expected):
        ''' Helper function for test_general_combination() '''
        query, commands, client_aliases, sys_message = master.parse_arguments(args)

        self.assertEqual(query, expected['query'])
        self.assertEqual(sys_message, expected['sys_message'])
        self.assertCountEqual(commands, expected['commands'])
        self.assertCountEqual(client_aliases, expected['client_aliases'])        

    def test_general_combinations(self):
        self.setUp_test_general_combinations()

        for case, pair in self.arg_pairs.items():
            args = pair[0]
            expected = pair[1]                                                    

            with self.subTest(case=case, args=args, expected=expected):
                self.compare(args, expected)

    def test_no_sys_message_provided(self):
        args = []
        args.append(SYS_COMMAND)
        
        unformatted_e_out = f"No sys message provided after arg {SYS_COMMAND}."

        self.compare_fatal_error_output(args, unformatted_e_out)

    def test_duplicate_arguments(self):
        commands = VALID_COMMANDS.copy()

        args = [TEST_ID, TEST_ID]

        unformatted_e_out = "Duplicate arguments provided."

        self.compare_fatal_error_output(args, unformatted_e_out)                

    def test_unknown_command(self):
        unknown_command = '-unknown_command'
        
        args = ["query", unknown_command]

        unformatted_e_out = f"Unknown command: {unknown_command}"

        
        self.compare_fatal_error_output(args, unformatted_e_out)

    def test_unknown_argument(self):
        unknown_arg = 'random'
        
        args = ["query", unknown_arg]

        unformatted_e_out = f'Unknown argument: {unknown_arg}'

        self.compare_fatal_error_output(args, unformatted_e_out)        

# Helper classes
class ArgPair:
    def __init__(self):
        self.arg_pair = [
            [], {'query': None,
            'sys_message': None,
            'commands': [], 
            'client_aliases': [] 
            }
        ]


if __name__ == '__main__':
    unittest.main(verbosity=2)