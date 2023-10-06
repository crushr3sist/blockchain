import socket
from zeroconf import ServiceBrowser, ServiceInfo, Zeroconf


class MyListener:
    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print(f"Service {name} added, service info: {info}")


# Define the IP address and port to connect to
ip_address = "192.168.1.100"
port = 12345

# Create a UDP socket and establish a connection
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.connect((ip_address, port))

# Now you can send and receive data over UDP
udp_socket.send(b"Hello, device!")
data, _ = udp_socket.recvfrom(1024)
print(f"Received data: {data.decode('utf-8')}")

# Initialize Zeroconf
zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_my_p2p_app._udp.local.", listener)

# Announce a custom UDP service
info = ServiceInfo(
    "_my_p2p_app._udp.local.",
    "My Device Name._my_p2p_app._udp.local.",
    port=12345,
    properties={"version": "1.0"},
)
zeroconf.register_service(info)

try:
    input("Press enter to exit...\n")
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()
