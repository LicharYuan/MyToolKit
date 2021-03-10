from MyToolKit.socket import Client


if __name__ == "__main__":
    HOST = "10.130.19.34"
    PORT = 6666
    action = "binary"
    value = "Test1231"
    client = Client(HOST, PORT, action, value)
    client.run()
