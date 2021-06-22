agents = {}


class ConnectionManager:
    def handle(self, msg):
        print(msg, type(msg))
        if msg['type'] in {'register', 'heartbeat'}:
            agents[msg['payload']['id']] = msg['payload']['hostname'], msg['payload']['ip']
        print(agents)
        return 'ack. {}'.format(msg)
