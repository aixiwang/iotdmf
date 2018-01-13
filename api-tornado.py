#-----------------------------------------------------------
# -*- coding: utf-8 -*- 
#-----------------------------------------------------------
# Copyright(c) 2015-2016 by Aixi Wang  <aixi.wang@hotmail.com>
#-----------------------------------------------------------

from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web
import os,time,sys
from tornado.escape import utf8
from hashlib import md5

#import web,time
from json import JSONDecoder, JSONEncoder
from pyiotlib import *

encoder = JSONEncoder()
decoder = JSONDecoder()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

import threading

from pointtool import *
import thread
import base64
import utils

##########################################################################
#                             Global Variables
##########################################################################
VERSION = 'V0.3'
IOT_DATA_SVR_IP = '127.0.0.1'

base_auth_user = 'xxx'
base_auth_passwd = 'xxx'

LOG_FILENAME = 'iotdmf.log.txt'

mutex1=threading.Lock()



settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "cookie_secret": base64.b64encode(base_auth_passwd),
    "login_url": "/login",
    "xsrf_cookies": False,
}

##########################################################################
#                             Global Functions
##########################################################################
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
    
#-------------------
# log_dump
#-------------------
def log_dump(filename,content):
    if os.name == "nt":
        fpath = '.\\' + filename
    else:
        fpath = './' + filename
    
    f = file(fpath,'ab')
    t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fs = f.write(t_s + '->' + str(content) + '\r\n')
    f.close()
    return
    



#-------------------
# get_jpg_jpg2_namelist
#-------------------    
def get_jpg_jpg2_namelist():
    os.system('rm -rf ./static/image')
    os.system('mkdir  ./static/image')
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)    
 
    seconds = 3600*24
    json_out = rpc.get_jpgs('*',time.time()-seconds,time.time())
    s = json_out['data']
    jpgs = []    
    for record in s:
        print record[0]
        r0 = record[0]
        print r0
        if r0.find(':') >= 0:
            id = r0.split(':')[1]
            f = float(r0.split(':')[2])      
            gmt = time.localtime(f)
            t_s = time.strftime('%Y-%m-%d-%H-%M-%S',gmt)
            t_s += '-' + str(f)
            s = 'image/' + id + '-' + t_s +'.jpg'
            name_item = {
                    'name': id + '-' + t_s +'.jpg',
                    'linkage': s
                    }            
            jpgs.append(name_item)
            print 'write jpg file:',s            
            writefile('./static/' + s,record[1].decode('hex'))
        else:
            print 'no valid data'
    
     
    json_out = rpc.get_jpgs2('*',time.time()-seconds,time.time())
    s = json_out['data']
    jpgs2 = []       
    for record in s:
        print record[0]
        r0 = record[0]
        print r0
        if r0.find(':') >= 0:
            id = r0.split(':')[1]
            f = float(r0.split(':')[2])      
            gmt = time.localtime(f)
            t_s = time.strftime('%Y-%m-%d-%H-%M-%S',gmt)
            s = 'image/unknown-' + id +'-' + t_s +'.jpg'
            name_item = {
                    'name': id + '-' + t_s +'.jpg',
                    'linkage': s,
            }            
            jpgs2.append(name_item)
            print 'write jpg2 file:',s
            writefile('./static/' + s,record[1].decode('hex'))
        else:
            print 'no valid data'

    res =  {
            'code':0,
            'jpgs': jpgs,
            'jpgs2': jpgs2,
        }            
    return encoder.encode(res)
    
#-------------------
# get_jpgmasks
#-------------------    
def get_jpgmasks():
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    s2 = rpc.get('jpgmask:12-12-12-12-12-12')
    return encoder.encode(s2)
    



#-------------------
# get_raw_data
#-------------------
def get_raw_data(tag,t):
    dp_set = get_group_points(tag)
    
    print 'dp_set:',dp_set   
    dp_set2 = [];
    if dp_set['code'] == 0:
        for dp_one in dp_set['data']:
            dp_set2.append(dp_one['id'])        
        print 'dp_set2:',dp_set2 

    
    
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
                
    json_out = rpc.get_datas('*',time.time()-t,time.time())
   
    
    
    print 'json_out:',json_out
    t_last = 0;
    if json_out['code'] == 0:   
        arr = []
        for record in json_out['data']:
            k = record[0]
            v = record[1]
            s = k.split(':')       
            res =  {
                'id': s[1],
                'time': s[2],
                'value': v
            }
            
            if s[1] in dp_set2:
                arr.append(res)

        res2 = {
            'code': 0,
            'data': arr,
        }
    else:
        res2 = {
            'code': -1,
            'data': 'error',
        }
    
    #return encoder.encode(res2)
    return res2

   
#-----------------------
# get_raw_data_stats
#-----------------------
def get_raw_data_stats(tag,t):

    dp_set = get_group_points(tag)
    print 'dp_set:',dp_set   
    dp_set2 = [];
    if dp_set['code'] == 0:
        for dp_one in dp_set['data']:
            dp_set2.append(dp_one['id'])        
        print 'dp_set2:',dp_set2 
    
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    #json_out = rpc.get_datas('P',time.time()-t,time.time())
    json_out = rpc.get_stats('*',time.time()-t,time.time())


    
         
    if json_out['code'] == 0:   
        arr = []
        for record in json_out['data']:
            k = record[0]
            v = record[1]
            s = k.split(':')       
            res =  {
                'id': s[1],
                'time': s[2],
                'value': v
            }
            
            if s[1] in dp_set2:
                arr.append(res)
                    
        res2 = {
            'code': 0,
            'data': arr,
        }
    else:
        res2 = {
            'code': -1,
            'data': 'error',
        }
    
    return encoder.encode(res2)
    
#-----------------------
# get_alarms
#-----------------------
def get_alarms(t):
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    json_out = rpc.get_alarms('*',time.time()-t,time.time())
    
    if json_out['code'] == 0:   
        arr = []
        for record in json_out['data']:
            k = record[0]
            v = record[1]
            s = k.split(':')       
            res =  {
                'name': s[1],
                'time': format_time_from_linuxtime(s[2]),
                'type': v
            }
            # latest, first
            arr.append(res)

        res2 = {
            'code': 0,
            'data': arr,
        }
    else:
        res2 = {
            'code': -1,
            'data': 'error',
        }
    
    return encoder.encode(arr[::-1])

#-----------------------------------
# get_power_cost_from_current_data
#-----------------------------------   
def get_power_cost_from_current_data(t):
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    json_out = rpc.get_stats('*',time.time()-t,time.time())
    
   
    if json_out['code'] == 0:   
        arr = []
        for record in json_out['data']:
            k = record[0]
            v = record[1]
            s = k.split(':')       
            res =  {
                'id': s[1],
                'time': s[2],
                'value': v
            }
            if s[1][0:4] == 'HOUR':
                #print res
                arr.append(res)

        res2 = {
            'code': 0,
            'data': arr,
        }
    else:
        res2 = {
            'code': -1,
            'data': 'error',
        }
    
    return res2

    
#-----------------------------------
# get_xxx_from_linuxtime
#----------------------------------- 
def get_hour_from_linuxtime(t):
    return time.localtime(float(t)).tm_hour
def get_min_from_linuxtime(t):
    return time.localtime(float(t)).tm_min 
def get_sec_from_linuxtime(t):
    return time.localtime(float(t)).tm_sec
def get_mday_from_linuxtime(t):
    return time.localtime(float(t)).tm_mday
def get_yday_from_linuxtime(t):
    return time.localtime(float(t)).tm_yday
def get_wday_from_linuxtime(t):
    return time.localtime(float(t)).tm_wday
def get_mon_from_linuxtime(t):
    return time.localtime(float(t)).tm_month
def get_year_from_linuxtime(t):
    return time.localtime(float(t)).tm_year
def get_isdst_from_linuxtime(t):
    return time.localtime(float(t)).tm_isdst
def format_time_from_linuxtime(t):
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t)))
    return s
    
#-----------------------------------
# get_linuxtime_from_str
#-----------------------------------    
def get_linuxtime_from_str(s):
    #'10:53:45 2013-10-21'
    struct_time = time.strptime(s,'%H:%M:%S %Y-%m-%d')
    t = time.mktime(struct_time)
    return t

#-----------------------------------
# power_low_price
#-----------------------------------     
def power_low_price():
    return 0.3070
    
#-----------------------------------
# power_high_price
#----------------------------------- 
def power_high_price():
    return 0.6170

#-----------------------------------
# get_power_price
#-----------------------------------    
def get_power_price(t):
    h = get_hour_from_linuxtime(t)
    if h >= 6 and h < 22:
        return power_high_price()
    else:
        return power_low_price()

#-----------------------------------
# caculate_power_cost
#-----------------------------------         
def caculate_power_cost(t1,t2,current):
    #print '>>>'
    #print format_time_from_linuxtime(t1),' ', format_time_from_linuxtime(t2)
    
    f = (t2-t1)*current*get_power_price(t2)*0.22/3600.0
    #print 'cost is :',f
    return f

#-----------------------------------
# gen_power_cost_stats
#-----------------------------------
def gen_power_cost_stats(t):
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    #print 'gen_24h_power_cost_stats is called'
    d = get_current_data(t)
    if d['code'] < 0:       
        res2 = {
                'code': -1,
                'data': [],
        }
        return encoder.encode(res2)
    
    arr = []
    t_last = 0
    
    f_day = 0;
    for record in d['data']:
        #print record

        
        #try:
        if 1:
            id = record['id']        
            t = float(record['time'])
            try:
                v = float(record['value'])
            except:
                print 'convert current data exception!'
                continue

            if id[0:2] == 'P-':
                id2 = 'HOUR' + '-' + id
                if t_last == 0:
                    t_last = t
                    continue
                else:
                    f = caculate_power_cost(t_last, t, v)
                    f_day = f_day + f
                    
                    if get_hour_from_linuxtime(t_last) != get_hour_from_linuxtime(t):
                        json_resp = rpc.save_stats(id2, str(t), str(f))
                        #print json_resp
                        #print 'save_stats:',id2,' ',str(t),' ',str(f)

                        res =  {
                            'id': id2,
                            'time': str(t),
                            'value': str(f)
                        }        
                        arr.append(res)
                        f_day = 0;

        #except:
        #    print 'processing data exception!'
        #    pass
        
        t_last = t
        
    res2 = {
        'code': 0,
        'data': arr,
    }
    return res2
    

#-----------------------------------
# gen_avg_stats
#-----------------------------------
def gen_avg_stats(t):
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)
        
    #print 'gen_24h_power_cost_stats is called'
    d = get_current_data(t)
    if d['code'] < 0:       
        res2 = {
                'code': -1,
                'data': [],
        }
        return encoder.encode(res2)
    
    arr = []
    t_last = 0
    
    f_day = 0;
    
    avg_dict = {}
    avg_t = time.time();
    
    for record in d['data']:
        #print record        
        id = record['id']        
        t = float(record['time'])
        try:
            v = float(record['value'])
        except:
            print 'convert current data exception!'
            continue
        if avg_dict.has_key(id) == False:
            avg_dict[id] = {}
            avg_dict[id]['v'] = v
            avg_dict[id]['cnt'] = 1
        else:
            avg_dict[id]['v'] += v
            avg_dict[id]['cnt'] += 1
        
    print 'avg_dict:',avg_dict
    
    for avg_id in avg_dict:
        #print 'avg_one:',avg_one
        avg_d = avg_dict[avg_id]['v']/avg_dict[avg_id]['cnt']
        json_resp = rpc.save_stats(avg_id, str(avg_t), str(avg_d))
        print 'save_stats:',avg_id,' ',str(avg_t),' ',str(avg_d)
        print json_resp

    return 0
    
#-----------------------------------
# gen_power_current_alarms
#----------------------------------- 
def gen_power_current_alarms(t):
    auth_key = readfile('./key.txt')
    rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
    if rpc.rpc == None:
        res2 = {
            'code': -1,
            'data': 'rpc call error',
        }
        return encoder.encode(res2)    
    #print 'gen_power_current_alarms is called'
    d = get_current_data(t)
    if d['code'] < 0:       
        res2 = {
                'code': -1,
                'data': [],
        }
        return encoder.encode(res2)
    
    arr = []
    t_last = 0
    v_last = 0
    flag = 0
    for record in d['data']:
        #print record
        #try:
        if 1:
            id = record['id']        
            t = float(record['time'])
            v = float(record['value'])
            if id[0:2] == 'P-':                
                # check posedge
                # print record
                if v >= 8 and v_last < 8:
                    print 'Hair drier ON'
                    json_resp = rpc.save_alarm(id, 'Hair drier ON',t)
                    print json_resp
                        
                # check negedge
                if v < 8 and v_last > 8:
                    print 'Hair drier OFF'
                    json_resp = rpc.save_alarm(id, 'Hair drier OFF',t)
                    print json_resp
 
                # check posedge
                if v >= 2.2 and v_last < 2.2 and v < 8:
                    print 'Bath heater ON'
                    json_resp = rpc.save_alarm(id, 'Bath heater ON 2',t)
                    print json_resp

                # check negedge
                if v < 2.2 and v_last > 2.2 and v < 8:
                    print 'Bath heater OFF'
                    json_resp = rpc.save_alarm(id, 'Bath heater OFF 2',t)
                    print json_resp

                v_last = v
                
                
        #except:
        #    print 'convert current data exception!'
        #    time.sleep(5)
        #    continue
        
    res2 = {
       'code': 0
    }
    return res2    

#----------------------
# stats_thread
#----------------------            
def stats_thread():
    cnt = 0;
    
    while True:
        print 'stats_thread.'
        try:
            
            gen_avg_stats(60)
            print 'gen_power_cost_stats(3600) executed.'
            

            cnt += 1
            if (cnt % 60) == 0:
                gen_power_cost_stats(3600)
                
           
            #auth_key = readfile('./key.txt')
            #rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
            #rpc.save_log('stats_thread','gen_power_cost_stats(3600)')

            time.sleep(60)                
            
        except:
            print 'stats_thread exception!'
            time.sleep(3)
            pass

#----------------------
# alarms_thread
#----------------------            
def alarms_thread():
    while 1:
        #try:
        #if 1:
            gen_power_current_alarms(3600)
            print 'gen_power_current_alarms(3600*24) executed.'
            
            auth_key = readfile('./key.txt')
            rpc = app_sdk(auth_key,server_ip=IOT_DATA_SVR_IP,server_port=7777)
            rpc.save_log('alarms_thread','gen_power_current_alarms(360)')
            time.sleep(1800)
        #except:
        #    print 'alarms_thread exception!'
        #    time.sleep(3)
        #    pass
        
#-------------------------
# start_background_thread
#-------------------------           
def start_background_thread():
    thread.start_new_thread(stats_thread,())
    #thread.start_new_thread(alarms_thread,())
    
    
#----------------------
# get_group_points
#----------------------       
def get_group_points(group):
    auth_key = readfile('./key.txt')
    pt_obj = pointtool(auth_key)
    pts = pt_obj.get_json_arr_points()
    arr = []
    for record in pts:
        #print '================================>'
        #print 'record:',record
        if record['group'] == group:
            arr.append(record)
            
    res2 = {
            'code': 0,
            'data': arr,
    }
    print 'arr:',arr
    
    return res2

#----------------------
# createpoint_json
#----------------------    
def createpoint_json(json_in):
    auth_key = readfile('./key.txt')
    pt_obj = pointtool(auth_key)
    id = json_in['id']
    group = json_in['group']
    description = json_in['description']
    retcode = pt_obj.createpoint(id,group,description)
    res2 = {
            'code': retcode
    }
    return res2

    
##########################################################################
#                             HTTP Handlers
##########################################################################
#-------------------
# BaseHandler
#-------------------
class BaseHandler(tornado.web.RequestHandler):
    #-------------------
    # get_current_user
    #-------------------
    def get_current_user(self):
        #print('get_current_user is called <---------------------')
        return self.get_secure_cookie("baseauth_user")

    #-------------------
    # base_auth_valid
    #-------------------
    def base_auth_valid(self):
        auth_header = self.request.headers.get('Authorization', None)
        from tornado.escape import utf8
        from hashlib import md5
        auth_mode, auth_base64 = auth_header.split(' ', 1)
        print('base_auth_valid ------->' + auth_mode + auth_base64)
        assert auth_mode == 'Basic'
        auth_username, auth_password = auth_base64.decode('base64').split(':', 1)
        if auth_username == base_auth_user and auth_password == base_auth_passwd:
            return True
        else:
            return False
            
    #-------------------
    # request_login
    #-------------------            
    def request_login(self):
        self.set_status(401)
        self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Login")    

#-------------------
# CookieTest
#------------------- 
class CookieTest(tornado.web.RequestHandler):
   def get(self):
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")

#-------------------
# login
#-------------------       
class login(BaseHandler):        
    def get(self):
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is not None:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            assert auth_mode == 'Basic'
            auth_username, auth_password = auth_base64.decode('base64').split(':', 1)
            if auth_username == base_auth_user or auth_password == base_auth_passwd:
                self.set_secure_cookie("baseauth_user", base_auth_user)
                self.redirect("/static/index.html")
            else:
                self.set_status(401)
                self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Login")
            
        else:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Login")

#-------------------
# test_async
#------------------- 
class test_async(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()



#---------------------------------
# URL- /environment/(.*)
#    ->/environment/1hour
#    ->/environment/1day
#    ->/environment/1week
#
# view_datapoints_handler
#----------------------------------     
class environment_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /environment/(.*)
        #----------------------
        print 'p1:',p1
        try:
            if p1 == '1hour':
                j = get_raw_data('environment',3600)
                s = encoder.encode(j)
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1day':
                j = get_raw_data_stats('environment',3600*24)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1week':
                j = get_raw_data_stats('environment',3600*24*7)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)
                
            else:
                self.redirect("/static/environment.html")
        except Exception as e:
            self.write('future_all exceptoin' + str(e))


#---------------------------------
# URL- /power/(.*)
#    ->/power/1hour
#    ->/power/1day
#    ->/power/1week
#
# view_datapoints_handler
#----------------------------------     
class power_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /current/(.*)
        #----------------------
        print 'p1:',p1
        try:
            if p1 == '1hour':
                j = get_raw_data('power',3600)
                s = encoder.encode(j)
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1day':
                j = get_raw_data_stats('power',3600*24)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1week':
                j = get_raw_data_stats('power',3600*24*7)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)
                
            else:
                self.redirect("/static/power.html")
        except Exception as e:
            self.write('future_all exceptoin' + str(e))

            

#---------------------------------
# URL- /future/(.*)
#    ->/future/1hour
#    ->/future/1day
#    ->/future/1week
#
# view_datapoints_handler
#----------------------------------     
class future_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /future/(.*)
        #----------------------
        print 'p1:',p1
        try:
            if p1 == '1hour':
                j = get_raw_data('future',3600)
                s = encoder.encode(j)
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1day':
                j = get_raw_data('future',3600*24)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)

            elif p1 == '1week':
                j = get_raw_data('future',3600*24*7)
                s = encoder.encode(j)            
                self.set_header('Access-Control-Allow-Origin','*')        
                self.write(s)
            else:
                self.redirect("/static/future.html")
        except Exception as e:
            self.write('future_all exceptoin' + str(e))
         
#-------------------
# /powercost
#-------------------
class power_cost(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        j2 = get_power_cost_from_current_data(3600*24*7)
        s = encoder.encode(j2)
        self.set_header('Access-Control-Allow-Origin','*')        
        self.write(s)

#-------------------
# /jpgnames
#-------------------
class jpgnames(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        s = get_jpg_jpg2_namelist()
        #raise web.seeother('/static/image')
        self.set_header('Access-Control-Allow-Origin','*')        
        self.write(s)

#-------------------
# /jpgmasks
#-------------------
class jpgmasks(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        s = get_jpgmasks()
        self.set_header('Access-Control-Allow-Origin','*')
        self.write(s)

#-------------------
# /testsig
#-------------------
class testsig(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_header('Access-Control-Allow-Origin','*')
        self.write(s)

#-------------------
# /newpowercost
#-------------------
class gen_power_cost(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        s = gen_power_cost_stats(3600*24*7)
        self.set_header('Access-Control-Allow-Origin','*')        
        self.write(s)

#-------------------
# /alarm
#-------------------
class alarm(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        s = get_alarms(3600*24)
        self.set_header('Access-Control-Allow-Origin','*')        
        self.write(s)

#---------------------------------
# URL- /datapoints/(.+)
#    ->/datapoints/environment
#    ->/datapoints/power
#    ->/datapoints/powercost
#
# view_datapoints_handler
#----------------------------------     
class view_datapoints(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /datapoints/*
        #----------------------
        print 'view_datapoints:', p1
        s = get_group_points(p1)        
        self.set_header('Access-Control-Allow-Origin','*')         
        s = encoder.encode(s)
        self.write(s)
    
    @tornado.web.authenticated        
    def post(self,p1):
        #----------------------
        # /datapoints/*
        #----------------------    
        post_in = self.request.body
        print 'post_in:',str(post_in)
        print('post_in:',post_in)
        json_in = decoder.decode(post_in)
        json_out =createpoint_json(json_in)
        s = encoder.encode(json_out)
        self.write(s)

#---------------------------------
# URL- /ops_all/(.*)
#    ->/ops_all/log_enable
#    ->/ops_all/log_disable
#    ->/ops_all/log_dump
#
# view_datapoints_handler
#----------------------------------     
class ops_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /view/datapoints/*
        #----------------------
        if p1 == 'log_enable':
            s = 'log_enable received!, TBD'
            print s
            self.write(s)

        if p1 == 'log_disable':
            s = 'log_disable received! TBD'
            print s
            self.write(s)

        if p1 == 'log_dump':
            try:
                log_txt = ''
                if has_file('./iotdmf.log.txt'):
                    log_txt = str(readfile('./iotdmf.log.txt'))
                if has_file('./../iot_data_svr/iot_data_svr.log.txt'):
                    log_txt += str(readfile('./../iot_data_svr/iot_data_svr.log.txt'))
                log_txt = log_txt.replace('\x0a','<br>');
                self.write(log_txt)
            except:
                self.write('log_dump fail')
                
        if p1 == 'sysinfo':
            try:
                log_txt = ''
                os.system('echo "----------------------------- PS -------------------" > sysinfo.txt')
                os.system('ps aux --sort=-%cpu >> sysinfo.txt')
                os.system('echo "------------------------------ DF -------------------" >> sysinfo.txt')
                os.system('df >> sysinfo.txt')
                os.system('echo "------------------------------ FREE ------------------" >> sysinfo.txt')
                os.system('free >> sysinfo.txt')
                
                if has_file('./sysinfo.txt'):
                    log_txt = str(readfile('./sysinfo.txt'))
                log_txt = log_txt.replace('\x0a','<br>')

                self.write(log_txt)          

            except:
                self.write('sysinfo fail') 
            
        if p1 == 'restart_host':
            s = 'restart_host received!'
            os.system("reboot -f &")
            print s
            self.write(s)

#---------------------------------
# URL- /dataprocess/(.*)
#    ->/dataprocess/load
#    ->/dataprocess/restart
#    ->/dataprocess/stop
#    ->/dataprocess/getlog
#    ->/dataprocess/delog
# view_datapoints_handler
#----------------------------------     
class dataprocess_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    @tornado.web.authenticated    
    def get(self,p1):
        #----------------------
        # /dataprocess/(.*) -- iotc1
        #----------------------
        if p1 == 'load':
            try:
                s = 'load'
                print s
                iotc_code = str(readfile('./../iotc/int.txt'))
                self.write(iotc_code)          
            except:
                self.write('load fail')          

        if p1 == 'start':
            s = ''
            print s
            try:
                pid = str(readfile('./../iotc/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                s = 'stop iotc ok, pid:' + pid + ','
            except:
                s = 'stop iotc fail,'
        
            try:
                os.system('./../iotc/start.sh')
                time.sleep(1)
                pid = str(readfile('./../iotc/iotc.pid'))
                s += 'start iotc ok, pid:' + pid
                self.write(s)
                
            except Exception as e:
                s += 'start iotc fail:' + str(e)
                self.write(s)

        if p1 == 'stop':
            s = 'stop'
            print s
            try:
                pid = str(readfile('./../iotc/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                self.write('stop iotc ok, pid:' + pid)
            except:
                self.write('stop iotc fail')            

        if p1 == 'getlog':
            try:
                log_txt = str(readfile('./../iotc/filesystem/log/iotc.log.txt'))
                log_txt = log_txt.replace('\x0a','<br>');
                
                self.write(log_txt)          
            except:
                self.write('getlog fail')          

        if p1 == 'delog':
            try:
                os.system('rm -rf ./../iotc/filesystem/log/iotc.log.txt');
                self.write('remove log ok')
                
            except:
                self.write('rmlog fail')          

                
        #----------------------
        # /dataprocess/(.*) -- iotc2
        #----------------------
        if p1 == 'load2':
            try:
                s = 'load'
                print s
                iotc_code = str(readfile('./../iotc2/int.txt'))
                self.write(iotc_code)          
            except:
                self.write('load fail')          

        if p1 == 'start2':
            s = ''
            print s
            try:
                pid = str(readfile('./../iotc2/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                s = 'stop iotc ok, pid:' + pid + ','
            except:
                s = 'stop iotc fail,'
        
            try:
                os.system('./../iotc2/start.sh')
                time.sleep(1)
                pid = str(readfile('./../iotc2/iotc.pid'))
                s += 'start iotc ok, pid:' + pid
                self.write(s)
                
            except Exception as e:
                s += 'start iotc fail:' + str(e)
                self.write(s)

        if p1 == 'stop2':
            s = 'stop'
            print s
            try:
                pid = str(readfile('./../iotc2/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                self.write('stop iotc ok, pid:' + pid)
            except:
                self.write('stop iotc fail')            

        if p1 == 'getlog2':
            try:
                log_txt = str(readfile('./../iotc2/filesystem/log/iotc.log.txt'))
                log_txt = log_txt.replace('\x0a','<br>');
                
                self.write(log_txt)          
            except:
                self.write('getlog fail')          

        if p1 == 'delog2':
            try:
                os.system('rm -rf ./../iotc2/filesystem/log/iotc.log.txt');
                self.write('remove log ok')
                
            except:
                self.write('rmlog fail')          


        #----------------------
        # /dataprocess/(.*) -- iotc3
        #----------------------
        if p1 == 'load3':
            try:
                s = 'load'
                print s
                iotc_code = str(readfile('./../iotc3/int.txt'))
                self.write(iotc_code)          
            except:
                self.write('load fail')          

        if p1 == 'start3':
            s = ''
            print s
            try:
                pid = str(readfile('./../iotc3/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                s = 'stop iotc ok, pid:' + pid + ','
            except:
                s = 'stop iotc fail,'
        
            try:
                os.system('./../iotc3/start.sh')
                time.sleep(1)
                pid = str(readfile('./../iotc3/iotc.pid'))
                s += 'start iotc ok, pid:' + pid
                self.write(s)
                
            except Exception as e:
                s += 'start iotc fail:' + str(e)
                self.write(s)

        if p1 == 'stop3':
            s = 'stop'
            print s
            try:
                pid = str(readfile('./../iotc3/iotc.pid'))
                print 'pid:',pid
                utils.kill_process(pid)
                self.write('stop iotc ok, pid:' + pid)
            except:
                self.write('stop iotc fail')            

        if p1 == 'getlog3':
            try:
                log_txt = str(readfile('./../iotc3/filesystem/log/iotc.log.txt'))
                log_txt = log_txt.replace('\x0a','<br>');
                
                self.write(log_txt)          
            except:
                self.write('getlog fail')          

        if p1 == 'delog3':
            try:
                os.system('rm -rf ./../iotc3/filesystem/log/iotc.log.txt');
                self.write('remove log ok')
                
            except:
                self.write('rmlog fail')          
                

    @tornado.web.authenticated        
    def post(self,p1):
        if p1 == 'upload':
            try:
                #self.write('upload post ok,' + self.get_argument('scode'))
                writefile('./../iotc/int.txt',self.get_argument('scode'))
                self.write('upload post ok')
            except:
                self.write('upload post fail')
        
        elif p1 == 'upload2':
            try:
                #self.write('upload post ok,' + self.get_argument('scode'))
                writefile('./../iotc2/int.txt',self.get_argument('scode'))
                self.write('upload post ok')
            except:
                self.write('upload post fail')
            
        elif p1 == 'upload3':
            try:
                #self.write('upload post ok,' + self.get_argument('scode'))
                writefile('./../iotc3/int.txt',self.get_argument('scode'))
                self.write('upload post ok')
            except:
                self.write('upload post fail')
        else:
            self.write('unsupported post method')

            
#---------------------------------
# URL- /devmgt/(.*)
#
# view_datapoints_handler
#----------------------------------     
class devmgt_all(BaseHandler):   
    #----------------------
    # get
    #----------------------
    def get(self,p1):
        print p1
        upload_path=os.path.join(os.path.dirname(__file__),'files')
        filepath=os.path.join(upload_path,p1 + '.cmd')
        #----------------------
        # /devmgt/(.*)
        #----------------------
        if has_file(filepath):
            s = readfile(filepath)
            print s
            self.write(s)
        else:
            s = 'echo devmgt cmd'
            print s
            self.write(s)

#------------------
# URL-/upload
# class upload_file
#------------------
class upload_file(BaseHandler):
    @tornado.web.authenticated        
    def post(self):
        upload_path=os.path.join(os.path.dirname(__file__),'files')
        print 'upload_path:',upload_path
        file_metas=self.request.files['filename']    
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:      
                up.write(meta['body'])
            #self.write('finished!')
            self.redirect("/static/file.html")            
            
#------------------
# URL-/download/(.*)
# class download_file
#------------------
class download_file(BaseHandler):
    @tornado.web.authenticated    
    def get(self,p1):
        filename = p1
        print('download file: ',filename)
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        upload_path=os.path.join(os.path.dirname(__file__),'files')
        filepath=os.path.join(upload_path,filename)
        if has_file(filepath):                
            s = readfile(filepath)
            self.write(s)
            print 'download finished'
        else:
            self.redirect("/static/file.html")
    
#-------------------
# MainHandler
#------------------- 
class index(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("/static/index.html")        

#-------------------
# routing
#-------------------
application = tornado.web.Application([
    (r"/", index),
    (r"/environment/(.*)", environment_all),
    (r"/power/(.*)", power_all),
    (r"/future/(.*)", future_all),    
    (r"/powercost", power_cost),
    (r"/newpowercost", gen_power_cost),
    (r"/alarm", alarm),
    (r"/datapoints/(.*)", view_datapoints),
    (r"/upload", upload_file),
    (r"/download/(.*)", download_file),
    (r"/ops/(.*)", ops_all),
    (r"/devmgt/(.*)", devmgt_all),
    (r"/dataprocess/(.*)", dataprocess_all),
    (r"/login", login),
],**settings)


##########################################################################
#                             M A I N
##########################################################################
if __name__ == "__main__":

    log_dump(LOG_FILENAME,'iotdmf started')

    # start iotc1
    s = ''
    try:
        os.system('./../iotc/start.sh')
        time.sleep(1)
        pid = str(readfile('./../iotc/iotc.pid'))
        s += 'start iotc ok, pid:' + pid
        print s
        log_dump(LOG_FILENAME,s)
    except Exception as e:
        s += 'start iotc fail:' + str(e)
        print s
        log_dump(LOG_FILENAME,s)

    # start iotc2
    s = ''
    try:
        os.system('./../iotc2/start.sh')
        time.sleep(1)
        pid = str(readfile('./../iotc2/iotc.pid'))
        s += 'start iotc2 ok, pid:' + pid
        print s
        log_dump(LOG_FILENAME,s)
    except Exception as e:
        s += 'start iotc2 fail:' + str(e)
        print s
        log_dump(LOG_FILENAME,s)


    # start iotc3
    s = ''
    try:
        os.system('./../iotc3/start.sh')
        time.sleep(1)
        pid = str(readfile('./../iotc3/iotc.pid'))
        s += 'start iotc3 ok, pid:' + pid
        print s
        log_dump(LOG_FILENAME,s)
    except Exception as e:
        s += 'start iotc3 fail:' + str(e)
        print s
        log_dump(LOG_FILENAME,s)

        
    try:
        start_background_thread()
        http_server = HTTPServer(application)
        http_server.listen(20000)
        print('IoT Data Management Framework API Server ' + VERSION + ' - Tornado version')       
        tornado.ioloop.IOLoop.instance().start()
        log_dump(LOG_FILENAME,'iotdmf stopped')
        
    except Exception as e:
        log_dump(LOG_FILENAME,'iotdmf stopped with exception:' + str(e))