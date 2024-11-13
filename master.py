import threading
import time

class HandleQuery:
    def __init__(self, session, console_lock):
        self.console_lock = console_lock
        self._stop_event = threading.Event()
        self.session = session

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def main(self):
        if not self.session.client.send_request():
            if self.stopped():
                return
            
            with self.console_lock:
                pass # send to UI that failed
            return
        
        self.session.client.format_response()

        if self.stopped():
            return

        with self.console_lock:
            pass # send self.session.client.response to UI
