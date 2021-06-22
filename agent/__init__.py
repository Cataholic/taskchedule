import threading
from .cm import ConnectionManager


class Agent:
    def __init__(self):
        self.event = threading.Event()
        self.cm = ConnectionManager()

    def start(self):
        while not self.event.is_set():  # 重连
            try:
                self.cm.start()
            except Exception as e:
                self.cm.shutdown()
            self.event.wait(3)

    def shutdown(self):
        self.event.set()
        self.cm.shutdown()
