from init_tests import append_to_path
append_to_path()
import unittest
import threading
import request_handler
import api_session
from constants import *

class _Master:
    def __init__(self):
        self.format = True

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        cli_lock = threading.Lock()
        master = _Master()
        self.request_handler = request_handler.RequestHandler(cli_lock, master)
        self._populate_sessions()
    
    def _populate_sessions(self, type=TYPE_TEST, n=1):
        self.request_handler.sessions = []
        
        type_to_client = {}
            
        for id, type in CLIENT_ID_TO_TYPE.items():
            if type in type_to_client.keys():
                type_to_client[type].append(id)
            else:
                type_to_client[type] = [id]
        
        for _ in range(n):
            client_id = type_to_client[type][0]
            session = api_session.Session(client_id)
            self.request_handler.sessions.append(session)

class TestRequest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main(verbosity=2)