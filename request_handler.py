import threading
import ui
import time

from constants import * ## Global constants

class RequestHandler:
    def __init__(self, cli_lock, parent):
        self.master = parent
        self.cli_lock = cli_lock
        self.requests_lock = threading.Lock()
        self.timer_active = True

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

            if self.timer_active:
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
        self.handler = parent
        self.master = self.handler.master

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def remove_from_requests(self):
        with self.handler.requests_lock:
            try:
                self.handler.requests.remove(self)
            except ValueError:
                pass

    def ask_to_remove_client(self):
        self.handler.timer_active = False
        
        # ! Lock does not encapsulate entire function since remove_client also requests lock.
        with self.handler.cli_lock:
            u_in = input(f"Do you wish to remove {self.session.client.name} from active sessions? (y/n)\n> ")
        
        if u_in.lower() in ['y', 'yes']:
            self.master.remove_client(self.session.client.name)
            
        self.handler.timer_active = True

    def print_removal_instructions(self):
        alias = self.master.client_to_alias(self.session.client.name)
        ui.c_out(f"You can remove '{self.session.client.name}' from active sessions using --rm:{alias} in your prompt, or try again.\n", 
                 bottom_margin=True)

    def main(self):
        try:
            successful_request = self.session.client.send_request()
        except Exception as e:
            with self.handler.cli_lock:
                ui.c_out("EXTERNAL ERROR: ",
                            color=DRED,
                            endline='')
                ui.c_out(e, 
                         color=YELLOW,
                         bottom_margin=True)

            self.ask_to_remove_client()
        
            self.remove_from_requests()
            return

        if self.session.type in STREAM_SUPPORT and self.session.client.stream_enabled:
            with self.handler.cli_lock:
                ui.c_out(f"Client: {self.session.client.name}", 
                         bottom_margin=True)
                
                try:
                    self.session.client.output_stream(format=self.master.format)
                    ui.c_out("End of stream.",
                             separator=True)
                except TypeError:
                    ui.c_out(f"Error encountered during streaming of response from {self.session.client.name}.", 
                             isolate=True, 
                             color=DRED,
                             separator=True)
                    self.print_removal_instructions()
                
            self.remove_from_requests()
            return

        if not successful_request:
            if not self.stopped():
                with self.handler.cli_lock:
                    ui.c_out(f"Client: {self.session.client.name}",
                             bottom_margin=True)
                    ui.c_out(f"No response received for '{self.sesion.client.name}'.",
                             separator=True)
                    self.print_removal_instructions()

            self.remove_from_requests()
            return
        
        self.session.client.format_response(format=self.master.format)

        if not self.stopped():
            with self.handler.cli_lock:
                ui.c_out(f"Client: {self.session.client.name}",
                         bottom_margin=True)
                ui.c_out(self.session.client.response,
                         separator=True)
        
        self.remove_from_requests()
