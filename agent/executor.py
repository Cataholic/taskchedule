import os
from subprocess import Popen, PIPE
from utils import getlogger
from config.base_dir import BASE_DIR

loggerpath = os.path.join(BASE_DIR, 'exec.log')
logger = getlogger(__name__, loggerpath)

class Executor:
    def run(self, script, timeout):
        proc = Popen(script, shell=True, stdout=PIPE)
        code = proc.wait(timeout)
        txt = proc.stdout.read()
        logger.info("{} {}".format(code, txt))
        return code, txt
