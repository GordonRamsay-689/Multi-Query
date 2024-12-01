import api_session
import google.generativeai
import threading
import ui
import time

from constants import * ## Global constants

class RequestHandler:
    def __init__(self, cli_lock, parent):
        self.parent = parent
        self.cli_lock = cli_lock
        self.requests_lock = threading.Lock()

        self.sessions = []
        self.requests = []

    def stop_threads(self): # Not in use yet
        with self.requests_lock:
            for request in self.requests:
                request.stop()
                self.requests.remove(request)

        for session in self.sessions:
            session.client.stop()

    def submit_requests(self, query):
        for session in self.sessions:
            session.client.query = query 

            # Create Request() and append to list of active requests
            request = Request(session, self)
            with self.requests_lock:
                self.requests.append(request)

            thread = threading.Thread(target=request.main, daemon=True) # Temporarily set daemon to false
            request.thread = thread            
            request.thread.start()

    def monitor_requests(self):
        start_time = time.time()

        while True:
            with self.requests_lock:
                if not self.requests:
                    return
                
            time.sleep(0.2)

            if (time.time() - start_time) > TIMEOUT:
                self.stop_threads()

                with self.cli_lock:
                    ui.c_out("Requests timed out.", isolate=True)
                
                return

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
                    ui.c_out(f"Client: {self.session.client.name}", bottom_margin=True)
                    ui.c_out("Failed to receive response.", separator=True)
        
            self.remove_from_requests()
            return
        
        self.session.client.format_response()

        if not self.stopped():
            with self.parent.cli_lock:
                ui.c_out(f"Client: {self.session.client.name}", bottom_margin=True)
                ui.c_out(self.session.client.response, separator=True)
        
        self.remove_from_requests()