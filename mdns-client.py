import socket
from zeroconf import Zeroconf, ServiceBrowser


class MyListener:
    def __init__(self, target_service_name):
        self.target_service_name = target_service_name
        self.target_info = None

    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        if name == self.target_service_name:
            self.target_info = zeroconf.get_service_info(type, name)
            print(f"Target service {name} added, info: {self.target_info}")


# Initialize Zeroconf
zeroconf = Zeroconf()
target_service_name = "My Device Name._my_p2p_app._udp.local."  # Replace with the target device's service name
listener = MyListener(target_service_name)
browser = ServiceBrowser(zeroconf, "_my_p2p_app._udp.local.", listener)

try:
    input("Press enter to discover and connect to the target device...\n")
    if listener.target_info:
        # Extract IP address and port from the target device's service info
        ip_address = socket.inet_ntoa(listener.target_info.address)
        port = listener.target_info.port
        print(f"Connecting to {ip_address}:{port} via UDP...")

        # Create a UDP socket and establish a connection
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.connect((ip_address, port))

        # Now you can send and receive data over UDP
        while True:
            message = input("Enter a message to send (or 'exit' to quit): ")
            if message.lower() == "exit":
                break
            udp_socket.sendto(message.encode("utf-8"), (ip_address, port))
            data, _ = udp_socket.recvfrom(1024)
            print(f"Received data: {data.decode('utf-8')}")

finally:
    zeroconf.close()
