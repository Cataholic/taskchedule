import datetime
import uuid
from .task import Task
from .agent import Agent
from config.state import *

class Storage:
    def __init__(self):
        self.agents = {}
        self.tasks = {}

    def reg_hb(self, payload):
        id = payload['id']
        self.agents[id] = {
            'heartbeat': datetime.datetime.now(),
            'info': payload,
            'busy': self.agents.get(id, {}).get('busy', False)
        }

    def get_agents(self):
        return list(self.agents.keys())

    def add_task(self, msg: dict):
        msg['task_id'] = uuid.uuid4().hex
        task = Task(**msg)
        self.tasks[task.id] = task
        return task.id

    def iter_tasks(self,):
        """过滤task状态"""
        yield from (task for task in self.tasks.values() if task.state in {WAITING, RUNNING})

    def get_task(self, agent_id):
        for task in self.iter_tasks():
            if agent_id in task.targets:
                if task.state == WAITING:
                    task.state = RUNNING
                task.targets[agent_id]['state'] = RUNNING
                return [task.id, task.script, task.timeout]

    def result(self, msg:dict):
        task = self.tasks[msg['id']]
        # TODO改变self.state
        agent = task.targets[msg['agent_id']]
        if msg['code'] == 0:
            agent['state'] = SUCCEED
        else:
            agent['state'] = FAILED


