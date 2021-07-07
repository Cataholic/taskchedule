import os
import uuid
import socket
import ipaddress
import netifaces


class Message:
    def __init__(self, myidpath):
        """从文件中读取主机的uuid"""
        if os.path.exists(myidpath):
            with open(myidpath) as f:
                self.id = f.readline().strip()
        else:
            self.id = uuid.uuid4().hex
            with open(myidpath, 'w') as f:
                f.write(self.id)

    def _get_addresses(self):
        """获取主机上所有接口可用的IPv4地址"""
        addresses = []

        for iface in netifaces.interfaces():
            ips = netifaces.ifaddresses(iface)
            if 2 in ips:
                for ip in ips[2]:
                    ip = ipaddress.ip_address(ip['addr'])
                    print(ip)
                    if ip.version != 4:  # 版本
                        continue
                    if ip.is_link_local:  # 169.254地址
                        continue
                    if ip.is_loopback:  # 回环
                        continue
                    if ip.is_multicast:  # 多播
                        continue
                    if ip.is_reserved:  # 保留
                        continue

                    addresses.append(str(ip))
        return addresses

    def reg(self):
        """生成注册信息"""
        return {
            "type": "register",
            "payload": {
                "id": self.id,
                "hostname": socket.gethostname(),
                "ip": self._get_addresses()
            }
        }

    def heartbeat(self):
        """生成心跳信息"""
        return {
            "type": "heartbeat",
            "payload": {
                "id": self.id,
                "hostname": socket.gethostname(),
                "ip": self._get_addresses()
            }
        }

    def result(self, task_id, code, output):
        return {
            "type": "result",
            "payload": {
                "id": task_id,
                "agent_id": self.id,
                "code": code,
                "output": output
            }
        }
