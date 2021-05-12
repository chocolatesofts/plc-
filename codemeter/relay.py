import socketserver
import sys
import socket

class Handler_TCPServer(socketserver.BaseRequestHandler):
    def nonblock_echo(self,sock1,sock2,bufflen=65536):
        data=b'0'
        try :
            data = sock1.recv(bufflen)
            if not data:
                return False,None
        except socket.timeout:
            return True,None
        sock2.sendall(data)
        return False,data

    def nonblock_isTerminated(self,resp):
        return resp[1]==None and resp[0]==False

    def handle(self):
        host_ip, server_port = sys.argv[3], int(sys.argv[4])
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.settimeout(10.0)
        try:
            tcp_client.connect((host_ip,server_port))
            tcp_client.settimeout(0.1)
            self.request.settimeout(0.1)
            while True:
                if self.nonblock_isTerminated(self.nonblock_echo(self.request,tcp_client)) :
                    break
                if self.nonblock_isTerminated(self.nonblock_echo(tcp_client,self.request)) :
                    break
        finally:
            tcp_client.close()

if __name__ == "__main__":
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    try:
        tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer,bind_and_activate=False)
        tcp_server.allow_reuse_address=True

        try :
            tcp_server.server_bind()
            tcp_server.server_activate()
            tcp_server.serve_forever()
        finally:
            tcp_server.shutdown()
            tcp_server.server_close()
            print("shutdown complete")
    finally:
        exit(1)
