import socket
import json
import os
import pathlib
import subprocess


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.255.255.255", 1))
        ip = s.getsockname()[0]
    except socket.error as e:
        ip = "127.0.0.1"
        raise e
    finally:
        s.close()
    return ip


class DHT:
    def __init__(self) -> None:
        self.path = os.environ.get("nuclei_discovery_server".upper())

    def initial_record(self):
        try:
            if os.environ.get("nuclei_discovery_server".upper()) != None:
                return
            else:
                setx_command = f'setx {"nuclei_discovery_server".upper()} "{pathlib.Path("./peer-data.json").absolute()}"'

                subprocess.call(setx_command, shell=True, stderr=subprocess.PIPE)

                with open(pathlib.Path("./peer-data.json"), "w+") as f:
                    f.write("{addresses:{}}")

        except KeyError:
            print(os.environ)
        finally:
            subprocess.call("refreshenv", shell=True, stderr=subprocess.PIPE)

    def give(self):
        with open(self.path, "r") as f:
            dht_content = f.read()
            print(dht_content)
            try:
                json_data = json.loads(dht_content)
                return json_data
            except json.JSONDecodeError as e:
                print(f"Failed to load JSON: {e}")

    def append(self, addr, port):
        dht_list = self.give()
        if "addresses" in dht_list:
            dht_list["addresses"].append(
                {
                    "address": f"{addr}",
                    "port": f"{port}",
                }
            )
        else:
            dht_list["addresses"] = [
                {
                    "address": f"{addr}",
                    "port": f"{port}",
                }
            ]
        with open(self.path, "w") as f:
            json.dump(dht_list, f, indent=4)


class Discovery:
    def __init__(self) -> None:
        self.peers = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = get_local_ip()
        self.port = 8000

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)

    def send_dht(self):
        ...

    def receive_discover_message(self):
        self.start()
