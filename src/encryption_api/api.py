"""Houses all of the encryption and decryption helper functions"""
import os
import json
from Crypto.Cipher import AES
from hashlib import sha256
import MasterConfig
from tqdm import tqdm
from encryption_api.Config import *


def pad_file(file):
    """Pad the file where necessary"""
    while len(file) % 16 != 0:
        file = file + b'0'
    return file


def encrypt_file(absolute_file_path, password='helloworld'):
    """Encrypt the contents of any file"""
    pswd = password.encode('utf-8')
    key = sha256(pswd).digest()
    mode = AES.MODE_CBC
    iv = 'this is an iv456'.encode('utf-8')  # 16 char string
    cipher = AES.new(key, mode, iv)

    with open(absolute_file_path, 'rb') as current_file:
        orig_contents = current_file.read()
    padded_contents = pad_file(orig_contents)
    encrypted_contents = cipher.encrypt(padded_contents)
    with open(absolute_file_path, 'wb') as current_file:
        current_file.write(encrypted_contents)


def decrypt_file(absolute_file_path, password='helloworld'):
    """Decrypt the contents of any file"""
    pswd = password.encode('utf-8')
    key = sha256(pswd).digest()
    mode = AES.MODE_CBC
    iv = 'this is an iv456'.encode('utf-8')  # 16 char string
    cipher = AES.new(key, mode, iv)

    with open(absolute_file_path, 'rb') as file:
        encrypted_contents = file.read()
    decrypted_contents = cipher.decrypt(encrypted_contents)
    with open(absolute_file_path, 'wb') as file:
        file.write(decrypted_contents.rstrip(b'0'))


def encrypt_private_folder():
    """Encrypt the contents of every file in the private_data folder"""
    password = PRIVATE_FOLDER_KEY.encode('utf-8')
    key = sha256(password).digest()
    mode = AES.MODE_CBC
    iv = 'this is an iv456'.encode('utf-8')  # 16 char string
    cipher = AES.new(key, mode, iv)

    print('Encrypting folder')
    private_dir = f'{MasterConfig.cwd}\\private_data'
    for root, dirs, files in os.walk(private_dir):
        for file in tqdm(files):
            with open(f'{private_dir}\\{file}', 'rb') as current_file:
                orig_contents = current_file.read()
            padded_contents = pad_file(orig_contents)
            encrypted_contents = cipher.encrypt(padded_contents)
            with open(f'{private_dir}\\{file}', 'wb') as current_file:
                current_file.write(encrypted_contents)


def decrypt_private_folder():
    """Decrypt the contents of every file in the private_data folder"""
    password = PRIVATE_FOLDER_KEY.encode('utf-8')
    key = sha256(password).digest()
    mode = AES.MODE_CBC
    iv = 'this is an iv456'.encode('utf-8')  # 16 char string
    cipher = AES.new(key, mode, iv)

    print('Decrypting folder')
    private_dir = f'{MasterConfig.cwd}\\private_data'
    for root, dirs, files in os.walk(private_dir):
        for file in tqdm(files):
            with open(f'{private_dir}\\{file}', 'rb') as current_file:
                encrypted_contents = current_file.read()
            decrypted_contents = cipher.decrypt(encrypted_contents)
            with open(f'{private_dir}\\{file}', 'wb') as current_file:
                current_file.write(decrypted_contents.rstrip(b'0'))


def check_encryption(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == 'status.json':
                # print('i found the status file')
                with open(f'{MasterConfig.cwd}\\private_data\\{file}', ) as status_file:
                    try:
                        data = json.load(status_file)
                    except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                        # print('folder is encrypted')
                        return True
                    else:
                        # print('folder is not encrypted')
                        return False


if __name__ == '__main__':
    MasterConfig.cwd = 'D:\\jarvis\\src'
    # encrypt_private_folder()
    # decrypt_private_folder()
