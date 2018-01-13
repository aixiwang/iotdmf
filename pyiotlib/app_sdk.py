#-----------------------------------------------------------
# BSD 3-clause license is applied to the code:
# http://opensource.org/licenses/BSD-3-Clause/
#
# Copyright (c) 2015 by Aixi Wang <aixi.wang@hotmail.com>
#-----------------------------------------------------------
import logging, random, time
import os
from RpcOnTcp import *

VERSION = 'v1'

class app_sdk:
    #---------------------------
    # __init__
    #---------------------------
    def __init__(self,auth_key,server_ip='127.0.0.1',server_port=7777):
        self.version = VERSION
        try:
            rpc = RpcOnTcp(auth_key,server_ip,server_port)
            self.rpc = rpc
        except:
            print 'app_sdk init exception!'
            self.rpc = None
            
    #---------------------------
    # set
    #---------------------------
    def set(self,k,v):
        json_in = {
                   'cmd':'set',
                   'k': k,
                   'v': v,
                  }
                                    
        json_out = self.rpc.call(json_in)
        return json_out
    #---------------------------
    # get
    #---------------------------
    def get(self,k):
        json_in = {
                   'cmd':'get',
                   'k': k
                  }
        json_out = self.rpc.call(json_in)
        return json_out
    #---------------------------
    # delete
    #---------------------------
    def delete(self,k):
        json_in = {
                   'cmd':'delete',
                   'k': k
                  }
        json_out = self.rpc.call(json_in)
        return json_out
    #---------------------------
    # save_log
    #---------------------------
    def save_log(self,name,data):      
        json_in = {
                 'cmd':'set_ts_data',
                 'tag': 'log',
                 'name': name,
                 'v': data,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_log
    #---------------------------
    def remove_log(self,name,t):
        k = 'log:' + name + ':' + str(t1)
        json_in = { 
                 'cmd':'delete',
                 'k':k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_logs
    #---------------------------        
    def get_logs(self,name,t1,t2):
        json_in = {
                 'key':'1234-5678',
                 'cmd':'get_ts_datas',
                 'tag': 'log',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_logs_keys
    #---------------------------        
    def get_logs_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_keys',
                 'tag': 'log',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out         
    #---------------------------
    # save_data
    #---------------------------
    def save_data(self,name,data,t='now'):
        if t == 'now':
            json_in = {
                     'cmd':'set_ts_data',
                     'tag': 'data',
                     'name': name,
                     'v': data,
                      }
        else:
            json_in = {
                     'cmd':'set_ts_data',
                     'tag': 'data',
                     'name': name,
                     't': str(t),
                     'v': data,
                      }
            
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_data
    #---------------------------
    def remove_data(self,name,t):
        k = 'data:' + name + ':' + str(t)
        json_in = { 
                 'cmd':'delete',
                 'k':k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_datas
    #---------------------------        
    def get_datas(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_datas',
                 'tag': 'data',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_datas_keys
    #---------------------------        
    def get_datas_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_keys',
                 'tag': 'data',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # save_stats
    #---------------------------
    def save_stats(self,name,time,data):
        json_in = {
                 'cmd':'set_stats_data',
                 'tag': 'data',
                 'name': name,
                 'time':time,
                 'v': data,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_stats
    #---------------------------
    def remove_stats(self,k):
        json_in = {
                 'cmd':'delete_stats',
                 'k': k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_stats
    #---------------------------        
    def get_stats(self,name,t1,t2):
        json_in = {
                 'cmd':'get_stats_datas',
                 'tag': 'data',
                 'name': name,
                 't1': t1,
                 't2': t2,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_stats_keys
    #---------------------------        
    def get_stats_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_stats_keys',
                 'tag': 'data',
                 'name': name,
                 't1': t1,
                 't2': t2,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out       
    #---------------------------
    # save_alarm
    #---------------------------        
    def save_alarm(self,name,data,t='now'):
        if t == 'now':
            json_in = {
                     'cmd':'set_ts_data',
                     'tag': 'alarm',
                     'name': name,
                     'v': data,
                      }
        else:
            json_in = {
                     'cmd':'set_ts_data',
                     'tag': 'alarm',
                     'name': name,
                     't': str(t),
                     'v': data,
                      }
                      
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_alarm
    #---------------------------
    def remove_alarm(self,name,t):
        k = 'alarm:' + name + ':' + str(t1)
        json_in = { 
                 'cmd':'delete',
                 'k':k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_alarms
    #---------------------------        
    def get_alarms(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_datas',
                 'tag': 'alarm',
                 'name': name,
                 't1': t1,
                 't2': t2,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out  
    #---------------------------
    # get_alarms_keys
    #---------------------------        
    def get_alarms_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_keys',
                 'tag': 'alarm',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out        
    #---------------------------
    # save_jpg
    #---------------------------
    def save_jpg(self,name,data):
        json_in = {
                 'cmd':'set_ts_data',
                 'tag': 'jpg',
                 'name': name,
                 'v': data,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_jpg
    #---------------------------
    def remove_jpg(self,name,t):
        k = 'jpg:' + name + ':' + str(t1)
        json_in = { 
                 'cmd':'delete',
                 'k':k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_jpgs
    #---------------------------        
    def get_jpgs(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_datas',
                 'tag': 'jpg',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_jpgs_keys
    #---------------------------        
    def get_jpgs_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_keys',
                 'tag': 'jpg',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out        
    #---------------------------
    # save_jpg2
    #---------------------------
    def save_jpg2(self,name,data):
        json_in = {
                 'cmd':'set_ts_data',
                 'tag': 'jpg2',
                 'name': name,
                 'v': data,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # remove_jpg2
    #---------------------------
    def remove_jpg2(self,name,t):
        k = 'jpg2:' + name + ':' + str(t1)
        json_in = { 
                 'cmd':'delete',
                 'k':k,
                  }
        json_out = self.rpc.call(json_in)     
        return json_out
    #---------------------------
    # get_jpgs2
    #---------------------------        
    def get_jpgs2(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_datas',
                 'tag': 'jpg2',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out 
    #---------------------------
    # get_jpgs_keys
    #---------------------------        
    def get_jpgs2_keys(self,name,t1,t2):
        json_in = {
                 'cmd':'get_ts_keys',
                 'tag': 'jpg2',
                 'name': name,
                 't1': t1,
                 't2': t2,
                   }
        json_out = self.rpc.call(json_in)     
        return json_out        
    #---------------------------
    # mqtt_pub
    #--------------------------- 
    def mqtt_pub(self,server_addr,server_port,username,password,topic,message):
        json_in = {
                   'cmd':'mqtt_pub',        
                   'server_addr':server_addr,
                   'server_port': server_port,
                   'username':username,
                   'password':password,
                   'topic':topic,                   
                   'message':message,
                  }
        json_out = self.rpc.call(json_in)        
        return json_out
    #---------------------------
    # setfile
    #--------------------------- 
    def setfile(self,filename,content):
        json_in = {
                   'cmd':'setfile',
                   'filename':filename,                   
                   'content':content,  
                  }

        json_out = self.rpc.call(json_in)        
        return json_out
    #---------------------------
    # getfile
    #--------------------------- 
    def getfile(self,filename):
        json_in = {
                   'cmd':'getfile',  
                   'filename':filename,
                   
                  }

        json_out = self.rpc.call(json_in)        
        return json_out
#----------------------
# main
#----------------------
if __name__ == "__main__":
    comport = readfile('./port.txt')
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,comport,115200)

    print '-------------------------------------'
    print 'test set'
    rpc.set('log','======asdfasdf=================')

    print '-------------------------------------'    
    print 'test get'
    json_out = rpc.get('log')
    print json_out
    
    print '-------------------------------------'
    print 'test delete'    
    json_out = rpc.delete('log')
    print json_out

    print '-------------------------------------'   
    print 'kv_get again'
    ret_code, v = rpc.get('log')
    print json_out

   
    print '-------------------------------------'    
    print 'test save_log, get_logs'
    # test save_log, get_logs
    i = 10
    while True:
        print 'i:',i
        rpc.save_log('test','adfasdfasdf')
        time.sleep(0.1)
        i -= 1
        if (i == 0):
            break;

    t = time.time() 
    json_out = rpc.get_logs('test',t-3,t)
    print json_out
    
    print 'test save_data, get_datas'                
    # test save_data, get_datas
    i = 10
    while True:
        print 'i:',i
        rpc.save_data('test','adfasdfasdf')
        time.sleep(0.1)
        i -= 1
        if (i == 0):
            break;
     
    t = time.time() 
    json_out = rpc.get_datas('test',t-3,t)
    print json_out
    
    print '-------------------------------------'
    print 'test save_alarm, get_alarms'                
    # test save_alarm, get_alarms
    i = 10
    while True:
        print 'i:',i
        rpc.save_alarm('test','adfasdfasdf')
        time.sleep(0.1)
        i -= 1
        if (i == 0):
            break;
     
    t = time.time() 
    json_out = rpc.get_alarms('test',t-3,t)
    print json_out 
    
    print '-------------------------------------'
    print 'test setfile'                
    content = 'test'.encode('hex')
    json_out = rpc.setfile('/test.txt',content)
    print json_out
    
    print '-------------------------------------'
    print 'test getfile'                
    json_out = rpc.getfile('./test.txt')
    print json_out
    
    