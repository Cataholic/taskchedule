import os
import zerorpc
import threading

from config.base_dir import BASE_DIR
from config.state import *
from .config import CONNECTIONURL
from utils import getlogger
from .message import Message
from .executor import Executor

loggerpath = os.path.join(BASE_DIR, 'agent.cm.log')
logger = getlogger(__name__, loggerpath)


class ConnectionManager:
    def __init__(self):
        self.client = zerorpc.Client()
        self.message = Message(os.path.join(BASE_DIR, 'myid'))

        self.event = threading.Event()
        self.state = WAITING  # 任务完成
        self.exec = Executor()

    def start(self, timeout=5):
        try:
            self.event.clear()  # 重置event
            self.client.connect(CONNECTIONURL)  # 建立连接
            logger.info(self.client.sendmsg(self.message.reg()))

            # 心跳循环
            while not self.event.wait(timeout):
                logger.info(self.client.sendmsg(self.message.heartbeat()))

                if self.state == WAITING:
                    task = self.client.get_task(self.message.id)
                    if task:
                        self.state = RUNNING
                        # [task.id, task.script, task.timeout]
                        code, output = self.exec.run(task[1], task[2])  # 阻塞
                        self.client.sendmsg(self.message.result(task[0], code, output))
                        self.state = WAITING

        except Exception as e:
            logger.error("{}".format(e))
            raise e

    def shutdown(self):
        self.event.set()
        self.client.close()
