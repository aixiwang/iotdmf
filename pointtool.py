# -*- coding=gbk -*- 
#-----------------------------------------------------------
# Copyright (c) 2015 by Aixi Wang <aixi.wang@hotmail.com>
#-----------------------------------------------------------

import random, time
import os
import sys
import uuid

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys
sys.path.append('../')

from pyiotlib import *
import time
import sys

from json import JSONDecoder, JSONEncoder
encoder = JSONEncoder()
decoder = JSONDecoder()

SERVER_IP = "127.0.0.1"
SERVER_PORT = 7777

#------------------------------
# unicode2hex
#------------------------------
def unicode2hex(utf_str):
    result = ""
    for i in utf_str:
        s1 = "%02x" % (ord(i) >> 8)
        s2 = "%02x" % (ord(i) & 0xFF)
        #print ord(i)
        #print s1,s2
        result += s1+s2
    return result

#------------------------------
# hex2unicode
#------------------------------    
def hex2unicode(hex_str):
    assert len(hex_str) % 4 == 0
    result = ""
    i=0
    length = len(hex_str)
    while i < length:
        result += unichr(int(hex_str[i:i+4],16))
        i += 4
    return result
        

class pointtool:
    #------------------------------
    # __init__
    #------------------------------
    def __init__(self,key,server_ip=SERVER_IP,server_port=SERVER_PORT):   
        self.rpc_handler = app_sdk(key,server_ip=SERVER_IP,server_port=SERVER_PORT)
        
    #------------------------------
    # db_set_points
    #------------------------------
    def db_set_points(self,pts):
        try:
            v = encoder.encode(pts)
            #print 'set_points, v:',v
            json_out = self.rpc_handler.set('config.point', v)
            print 'set_points:',json_out
            return 0            
        except:
            return -1
        
    #------------------------------
    # db_get_points
    #------------------------------
    def db_get_points(self):
        json_out = self.rpc_handler.get('config.point')
        print 'get_points:',json_out
        if json_out['code'] < 0:
            return {}
        else:
            v = json_out['data']['v']
            if len(v) > 0:
                #print 'v:',v
                #print 'type:',type(v)
                result, index = decoder.raw_decode(v)
                #print 'result:',result
                #print 'index:',index
                return result
            else:
                return {}

    #------------------------------
    # rm_points
    #------------------------------
    def rm_points(self,k):
        global rpc_handler
        json_out = self.rpc_handler.delete('config.point')
        v = json_out['code']
        return v

    #------------------------------
    # list_points
    #------------------------------
    def list_points(self):
        #print 'list_points is called'
        pts = self.db_get_points()
        #print 'pts:',pts
        for pt in pts.iteritems():
            try:
                #print pt
                v1 = pt[1].split('~')[0]
                v2 = pt[1].split('~')[1]        
                v_u = hex2unicode(v2)
                #print 'id:',pt[0]
                #print 'group:',v1
                #print 'description:',v_u.encode('gbk')
            except:
                pass

    #------------------------------
    # get_json_arr_points
    #------------------------------
    def get_json_arr_points(self):
        #print 'get_json_points is called'
        pts = self.db_get_points()
        #print 'pts:',pts
        arr = []
        for pt in pts.iteritems():
            try:
                #print pt
                v1 = pt[1].split('~')[0]
                v2 = pt[1].split('~')[1]        
                
                if len(pt[0]) > 0:
                    res =  {
                            'id': pt[0],
                            'group': v1,
                            'description': v2,
                        }                
                    arr.append(res)
            except:
                pass
        return arr
                
    #------------------------------
    # add_point
    #------------------------------
    def add_point(self,k,v):
        #print 'add_point is called'

        pts = self.db_get_points()
        #print 'pts 1:',pts
        pts[k] = v
        #print 'pts 2:',pts
        retcode = self.db_set_points(pts)
        return retcode

    #------------------------------
    # del_point
    #------------------------------
    def del_point(self,k):
        #print 'del_point is called, k:',k
        pts = self.db_get_points()
        #print 'pts 1:',pts
        if pts.has_key(k):
            pts.pop(k)
        #print 'pts 2:',pts
        self.db_set_points(pts)

    #------------------------------
    # set_point
    #------------------------------
    def set_point(self,k,v):
        #print 'set_point is called'
        pts = self.db_get_points()
        #print 'pts 1:',pts
        pts[k] = v
        #print 'pts 2:',pts
        self.db_set_points(pts)

    #------------------------------
    # get_point
    #------------------------------
    def get_point(self,k):
        #print 'get_point is called'
        pts = self.db_get_points()
        #print 'pts 1:',pts
        v = pts[k]
        return v
        
    #------------------------------
    # help
    #------------------------------    
    def help(self):
        print 'supported commands:'
        print '1.listpoints'    
        print '2.createpoint'
        print '3.getpoint'
        print '4.setpoint'
        print '5.delpoint'    
        print '6.help'

    #------------------------------
    # createpoint
    #------------------------------     
    def createpoint_shell(self):
        k = raw_input('please input point id:')
        g = raw_input('please input data group:')        
        v = raw_input('please input point description:')
        
        v2 = v.decode('gbk')   
        v3 = unicode2hex(v2)
        self.add_point(k,g + '~' + v3)
        #v = self.get_point(k)
        #print v
        #v_u = hex2unicode(v)
        #print 'v len:',len(v_u)
        #print 'k:',k,' v:',v_u.encode('gbk')
        pass

    #------------------------------
    # createpoint
    #------------------------------     
    def createpoint(self,k,g,v):
        #try:
        #    v2 = v.decode('gbk')
        #except:
        #    v2 = v.decode('utf-8')
        print 'v:',v
        if isinstance(v, unicode) != True:
            return -1
        
        v3 = unicode2hex(v)
        retcode = self.add_point(k,g + '~' + v3)
        #v = self.get_point(k)
        #print v
        #v_u = hex2unicode(v)
        #print 'v len:',len(v_u)
        #print 'k:',k,' v:',v_u.encode('gbk')
        return retcode     
    #------------------------------
    # getpoint
    #------------------------------      
    def getpoint_shell(self):
        k = raw_input('please input point id:')
        v = self.get_point(k)
        try:
            v1 = v.split('~')[0]
            v2 = v.split('~')[1]
            #print v
            v_u = hex2unicode(v1)
            #print 'v len:',len(v_u)
            print 'id:',k
            print 'group:',v1
            print 'description',v_u.encode('gbk')
        except:
            print 'get point error!'

    #------------------------------
    # deletepoint
    #------------------------------       
    def deletepoint_shell(self):
        self.list_points()
        k = raw_input('please input point id to delete:')
        self.del_point(k)
        self.list_points()
    #------------------------------
    # listpoints
    #------------------------------     
    def listpoints_shell(self):   
        self.list_points()
        
#----------------------
# main
#----------------------
if __name__ == "__main__":
    global rpc_handler
    print 'point tool v0.2 (leveldb), ctrl+c to exit.'
    key = raw_input('key:')

    while(1):
        print '---------------------------------------------'
        cmd = raw_input('please input your command:')
        if (cmd == 'listpoints' or cmd == '1'):
            p = pointtool(key)        
            p.listpoints_shell()        
        elif (cmd == 'createpoint' or cmd == 'setpoint' or cmd == '2'  or cmd == '4'):
            p = pointtool(key)        
            p.createpoint_shell()
        elif (cmd == 'getpoint'  or cmd == '3'):
            p = pointtool(key)        
            p.getpoint_shell()
        elif (cmd == 'delpoint'  or cmd == '5'):
            p = pointtool(key)
            p.deletepoint_shell()
        else:
            p = pointtool(key)
            p.help()
