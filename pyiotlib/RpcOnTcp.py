#-----------------------------------------------------------
# BSD 3-clause license is applied to the code:
# http://opensource.org/licenses/BSD-3-Clause/
#
# Copyright (c) 2015 by Aixi Wang <aixi.wang@hotmail.com>
#-----------------------------------------------------------

import socket
import time
#import serial
#import hashlib
import os
from json import JSONDecoder, JSONEncoder

encoder = JSONEncoder()
decoder = JSONDecoder()

#------------------------------------------
# common utils routines
#------------------------------------------
def readfile(filename):
    f = file(filename,'rb')
    fs = f.read()
    f.close()
    return fs

def writefile(filename,content):
    f = file(filename,'wb')
    fs = f.write(content)
    f.close()
    return
    
def has_file(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

def remove_file(filename):
    if has_file(filename):
        os.remove(filename)
        
def anykey():
    s = raw_input('any key to contiue...')
       
class RpcOnTcp:
    def __init__(self,auth_key,server_ip,server_port):
        self.auth_key = auth_key
        self.server_ip = server_ip
        self.server_port = server_port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (server_ip, server_port)
        s.connect(address)
        self.tcp_s = s
       
    #----------------------
    # pack_json
    # input dict, output str
    #----------------------
    def pack_jsonstr(self,s):
        s1 = encoder.encode(s)
        new_s = '*' + str(len(s1)) + '\r\n' + s1
        return new_s

    #----------------------
    # unpack_json
    # input str, output dict
    #----------------------
    def unpack_jsonstr(self,s):
        s_dict = decoder.decode(s)
        return s_dict

    def loop_read_response_package(self):
        #-----------------------------------------------
        while True:
            self.tcp_s.setblocking(1)
            # wait for *
            k1 = 1000
            while k1:
                d1 = self.tcp_s.recv(1)
                if len(d1)>0:
                    if (d1 == '*'):
                        break;
                    else:
                        time.sleep(0.01)
                        k1 -= 1
                else:
                    time.sleep(0.01)
                    k1 -= 1
            if k1 == 0:
                return -1,'waiting for * error exception'        
            k1 = 1000
            lens = ''
            while k1:
                d1 = self.tcp_s.recv(1)
                if len(d1)>0:
                    if d1 != '\r':
                        lens += d1
                    else:
                        break;
                else:
                    time.sleep(0.01)
                    k1 -= 1
            if k1 == 0:
                return -1,'waiting for escape r error exception'
            try:
                block_len = int(lens)
            except:
                return -1,''                  
            # wait for \n
            k1 = 1000
            while k1:
                d1 = self.tcp_s.recv(1)
                if len(d1)>0:
                    if d1 != '\n':
                        return -1,'waiting for change line char error'                    
                    else:
                        break;
                else:
                    time.sleep(0.01)
                    k1 -= 1
            if k1 == 0:
                return -1,'waiting for change line char error timeout'
            data_buff = ''
            k1 = 10000
            while block_len and k1:
                data = self.tcp_s.recv(block_len)
                if len(data) > 0:
                    data_buff += data
                    block_len -= len(data)
                else:
                    time.sleep(0.01)
                    k1 -= 1
            if k1 == 0 or block_len != 0:
                return -1,'waiting for data timeout'
            try:      
                return 0, data_buff
            except:
                return -1,'data block error exception'
        #----------------------------------------------- 
    def call(self,dict_in):
        try:
            dict_in['key'] = self.auth_key
            s = self.pack_jsonstr(dict_in)
            self.tcp_s.send(s)
            retcode,data_buff = self.loop_read_response_package()
            if (retcode == 0):
                resp_dict = self.unpack_jsonstr(data_buff)
                return resp_dict            
            else:
                return {'code':-1,'data': data_buff}
        except:
            return {'code':-1,'data': 'call exception'}