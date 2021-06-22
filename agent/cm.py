import os
import zerorpc
import threading

from .config import CONNECTIONURL
from utils import getlogger
from .message import Message

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
loggerpath = os.path.join(BASE_DIR, 'agent.cm.log')
logger = getlogger(__name__, loggerpath)


class ConnectionManager:
    def __init__(self):
        self.client = zerorpc.Client()
        self.message = Message(os.path.join(BASE_DIR, 'myid'))
        self.event = threading.Event()

    def start(self, timeout=5):
        try:
            self.event.clear()
            self.client.connect(CONNECTIONURL)  # 建立连接
            logger.info(self.client.sendmsg(self.message.reg()))

            # 心跳循环
            while not self.event.wait(timeout):
                logger.info(self.client.sendmsg(self.message.heartbeat()))
        except Exception as e:
            logger.error("{}".format(e))
            raise e

    def shutdown(self):
        self.event.set()
        self.client.close()

