import socket
from datetime import datetime


class Handler_Dojo:


    def receive_connection(self):
        data = ''
        addr = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.bind(('', 443))
            client_socket.listen(2)
            conn, addr = client_socket.accept()
            with conn:
                print('[+] Connection: ', addr, ' [+]\n\n\n')
                while True:
                    data = conn.recv(1024)
                    return data, addr


    def create_write_file(self, data, addr):
        date = datetime.now().strftime('%d%m%y-%H%M')
        addrs = addr[0].split('.')
        name = 'log-{}-{}-{}-{}-{}'.format(date, addrs[0], addrs[1], addrs[2], addrs[3])
        with open(name, 'w') as file:
            file.write(data.decode('utf-8'))



