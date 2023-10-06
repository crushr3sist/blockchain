import json
import random
import socket
import sys
import threading
import time


import socket
import threading
import json


class PeerSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen(5)

    def connect(self, target_host, target_port):
        try:
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((target_host, target_port))
            return target_socket
        except ConnectionRefusedError as e:
            print(e)
            print(f"Connection to {target_host}:{target_port} failed.")

    def listen_for_messages(self):
        while True:
            client_socket, _addr = self.socket.accept()
            message = client_socket.recv(1024).decode()
            print(f"received message: {message}")
            client_socket.close()

    def send_message(self, target_socket, message):
        target_socket.send(message.encode())


class Peer(PeerSocket):
    def __init__(self, peer_id, host, broadcast_port, listen_port):
        super().__init__(host, listen_port)
        self.peer_id = peer_id
        self.known_peers = set()
        self.broadcast_port = broadcast_port
        self.peers = {}

    def broadcast_discovery(self):
        print("start discover")
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        ) as udp_socket:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            udp_socket.bind(("0.0.0.0", self.broadcast_port))
            while True:
                discovery_message = {
                    "peer_id": self.peer_id,
                    "host": self.host,
                    "port": self.port,
                }
                udp_socket.sendto(
                    json.dumps(discovery_message).encode(), ("10.1.1.255", self.port)
                )
                threading.Event().wait(5)
                if self.peers["peers"] != None:
                    break

    def listen_for_discovery(self):
        print("start listen")
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        ) as udp_socket:
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            udp_socket.bind(("0.0.0.0", self.port))
            while True:
                data, (source_ip, _source_port) = udp_socket.recvfrom(1024)
                if source_ip == self.host:
                    print("true")
                    continue
                discovery_message = json.loads(data.decode())
                peer_id = discovery_message["peer_id"]

                print(self.known_peers)
                self.known_peers.add(peer_id)
                print(
                    f"Discovered peer: {peer_id} at {discovery_message['host']}:{discovery_message['port']}"
                )
                self.peers["peers"] = {
                    "ip": discovery_message["host"],
                    "port": discovery_message["port"],
                }
                if self.peers["peers"] != None:
                    break

    def connection_loop(self):
        while True:
            threading.Thread(target=self.broadcast_discovery).start()
            threading.Thread(target=self.listen_for_discovery).start()
            time.sleep(10)
            self.start()
            print(self.peers)
            self.connect(self.peers["peers"]["ip"], self.peers["peers"]["port"])
            self.listen_for_messages()
            self.send_message()


if __name__ == "__main__":
    peer1 = Peer("peer1", "10.1.1.140", 5001, 5002)
    peer1.connection_loop()
