from subprocess import Popen, PIPE


class Executor:
    def run(self, script, timeout):
        proc = Popen(script, shell=True, stdout=PIPE)
        code = proc.wait(timeout)
        txt = proc.stdout.read()
        return code, txt
