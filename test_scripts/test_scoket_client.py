from MyToolKit.socket import Client
import time

if __name__ == "__main__":
    HOST = "10.130.19.34"
    PORT = 6666
    action = "search"
    value = "net"
    for i in range(2):
        client = Client(HOST, PORT, action, value+str(i))
        client.run()
        print("rec:", client.recv_info)
