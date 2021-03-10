import socket
import selectors
from .lib import ServerMessage
import traceback

class Server(object):
    """ Multi-connection """
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel  = selectors.DefaultSelector()

        self.sock.bind((host, port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)

    def accept_wrapper(self, accpet_sock):
        conn, addr = accpet_sock.accept()  
        print("accepted connection from", addr)
        conn.setblocking(False) 
        message = ServerMessage(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)
    
    def run(self):
        try:
            while True:
                # waiting connection
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                "main: error: exception for",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()

        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting server")
        finally:
            self.sel.close()

    


    





