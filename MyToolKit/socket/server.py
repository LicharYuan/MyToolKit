import socket
import selectors
from .lib import ServerMessage
import traceback
from MyToolKit.utils import append_to_txt
import time, os

class Server(object):
    """ Multi-connection """
    def __init__(self, host, port, save=True):
        super().__init__()
        self.host = host
        self.port = port
        self.save = save
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sel  = selectors.DefaultSelector()

        self.sock.bind((host, port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, data=None)
        if save:
            self._save_file = os.path.join(os.getcwd(), time.strftime('%Y%m%d%H%M')+f"_{port}.txt")

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
                            if self.save and mask==1:
                                # avoid repeat save
                                self.save_events(message)
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

    def save_events(self, message):
        try:
            content = message.request
            request_type = message.jsonheader.get("content-type")
            if "json" in request_type:
                raise NotImplementedError("Json is not support to save")
            print(type(content), request_type)
            str_content = content.decode("utf-8")
            val_content = str_content.split(">>")[-1][1:]
            append_to_txt(self._save_file, val_content)
            print(f"message append to {self._save_file}")
        except NotImplementedError:
            print("Save failed, Not support json type")
        finally:
            print("Exit saving message")
