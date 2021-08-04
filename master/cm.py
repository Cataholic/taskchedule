import os
from .storage import Storage
from utils import getlogger
from config.base_dir import BASE_DIR

logger = getlogger(__name__, os.path.join(BASE_DIR, 'master.cm.log'))


class ConnectionManager:
    def __init__(self):
        self.storage = Storage()

    def handle(self, msg):
        logger.info(type(msg))
        try:
            if msg['type'] in {'register', 'heartbeat'}:
                self.storage.reg_hb(msg['payload'])
                logger.info("{}".format(self.storage.agents))
            elif msg['type'] == 'result':
                self.storage.result(msg['payload'])

            print(self.storage.get_agents())
            return "ack. {}".format(msg)
        except Exception as e:
            print(e)
            logger.error("".format(e))
            return "Bad Request."

    sendmsg = handle  # agent.cm接口

    def add_task(self,msg):
        return self.storage.add_task(msg)

    def get_task(self, agent_id):
        return self.storage.get_task(agent_id)

    def get_agents(self):
        return self.storage.get_agents()
