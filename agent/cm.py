import os
import zerorpc
import threading

from .config import CONNECTIONURL
from utils import getlogger
from .message import Message

loggerpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agent.cm.log')

logger = getlogger(__name__, loggerpath)


class ConnectionManager:
    def __init__(self):
        self.client = zerorpc.Client()
        self.message = Message()
        self.event = threading.Event()

    def start(self, timeout=5):
        try:
            self.event.clear()
            self.client.connect(CONNECTIONURL)  # 建立连接
            logger.info(self.client.sendmsg(self.message.reg()))

            while not self.event.wait(timeout):
                logger.info(self.client.sendmsg(self.message.heartbeat()))
        except Exception as e:
            logger.error("{}".format(e))
            raise e

    def shutdown(self):
        self.event.set()
        self.client.close()
