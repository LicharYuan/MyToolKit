from MyToolKit.socket import Server


if __name__ == "__main__":
    HOST = "10.130.19.34"
    PORT = 6666
    server = Server(HOST, PORT)
    server.run()

