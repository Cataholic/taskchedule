import zerorpc


MASTERURL = "tcp://0.0.0.0:9000"

class Master:
    def sendmsg(self, msg):
        print(msg)
        return 'ack. hello {}'.format(msg)

server = zerorpc.Server(Master())
server.bind(MASTERURL)
server.run()

print('~~~~~~~~~')


