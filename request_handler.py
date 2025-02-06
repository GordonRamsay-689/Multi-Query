import threading
import ui
import time

from openai import NotFoundError
from google.api_core.exceptions import NotFound

from constants import * ## Global constants

class RequestHandler:
    def __init__(self, cli_lock, parent):
        self.parent = parent
        self.cli_lock = cli_lock
        self.requests_lock = threading.Lock()

        self.sessions = []
        self.requests = []

    def stop_threads(self):
        with self.requests_lock:
            for request in self.requests:
                request.stop()
                self.requests.remove(request)

        for session in self.sessions:
            session.client.stop()

    def submit_requests(self, query):
        for session in self.sessions:
            session.client.set_query(query)

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
                    ui.c_out("Requests timed out.",
                             color=DRED,
                             isolate=True)
                
                return

class Request:
    def __init__(self, session, parent):
        self._stop_event = threading.Event()
        self.session = session
        self.parent = parent
        self.master = parent.parent

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
        except (NotFoundError, NotFound):
            with self.parent.cli_lock:
                ui.c_out("You do not have permission to use this model: ", 
                         color=DRED, 
                         endline='')
                ui.c_out(f"{self.session.client.name}")
                ui.c_out(f"You can remove it using --rm:{self.session.client.name} or try again.\n", 
                         color=DRED,
                         bottom_margin=True)
                
            self.remove_from_requests()
            return
        except Exception as e:
            pass # Log exception. 
            successful_request = False

        if self.session.type in STREAM_SUPPORT and self.session.client.stream_enabled:
            with self.parent.cli_lock:
                ui.c_out(f"Client: {self.session.client.name}", 
                         bottom_margin=True)
                
                try:
                    self.session.client.output_stream(self.master.format)
                    ui.c_out("End of stream.",
                             separator=True)
                except TypeError:
                    ui.c_out("Failed to stream response.", 
                             isolate=True, 
                             color=DRED,
                             separator=True)
                
            self.remove_from_requests()
            return

        if not successful_request:
            if not self.stopped():
                with self.parent.cli_lock:
                    ui.c_out(f"Client: {self.session.client.name}",
                             bottom_margin=True)
                    ui.c_out("Failed to receive response.",
                             separator=True)
        
            self.remove_from_requests()
            return
        
        self.session.client.format_response(format=self.master.format)

        if not self.stopped():
            with self.parent.cli_lock:
                ui.c_out(f"Client: {self.session.client.name}",
                         bottom_margin=True)
                ui.c_out(self.session.client.response,
                         separator=True)
        
        self.remove_from_requests()