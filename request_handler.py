import api_session
import google.generativeai
import threading
import ui
# import time

from constants import * ## Global constants

class RequestHandler:
    def __init__(self, cli_lock):
        self.cli_lock = cli_lock
        self.requests_lock = threading.Lock()

        self.sessions = []
        self.requests = []

    def stop_threads(self): # Not in use yet
        for request in self.requests:
            request.stop()

    def submit_requests(self, query):
        for session in self.sessions:
            session.client.query = query 

            # Create Request() and append to list of active requests
            request = Request(session, self)
            with self.requests_lock:
                self.requests.append(request)

            thread = threading.Thread(target=request.main, daemon=False) # Temporarily set daemon to false
            request.thread = thread            
            request.thread.start()
        
    def join_requests(self): # For use when run with args
        for request in self.requests:
            request.thread.join()
            

class Request:
    def __init__(self, session, parent):
        self._stop_event = threading.Event()
        self.session = session
        self.parent = parent

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def remove_from_requests(self):
        with self.parent.requests_lock:
            try:
                self.parent.requests.remove(self)
            except ValueError:
                pass

    def main(self):
        try:
            successful_request = self.session.client.send_request()
        except Exception as e:
            successful_request = False

        if not successful_request:
            if not self.stopped():
                with self.parent.cli_lock:
                    print("failed to receive response") # Debug
                    print(self.session.name) # Debug
                    pass # send to UI that failed   
        
            self.remove_from_requests()
            return
        
        self.session.client.format_response()

        if not self.stopped():
            with self.parent.cli_lock:
                ui.c_out(f"Client: {self.session.name}", bottom_margin=True)
                ui.c_out(self.session.client.response, separator=True)
        
        self.remove_from_requests()
        return