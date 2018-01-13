#!/usr/bin/python
#---------------------------------------------
# Gateway Management Agent (Python Version)
#--------------------
import os
import sys
import time
import logging
#import simplejson
import json
#from aes256crypto import *
#from crypto_dummy import *
import urllib2
import pyiotlib

shared_data = [[],[],[],[],[],[],[],[]]


#--------------------
# cache_shared_data
# i : index
#--------------------
def cache_shared_data(i,d,w):
    global shared_data
    if i < 0 or i > 7:
        print 'invalid index'
        return -1
        
    if len(shared_data[i]) == w:
        shared_data[i].pop(0)
        shared_data[i].append(d)        
    elif len(shared_data[i]) > w:
        shared_data[i].pop(0)
    else:
        shared_data[i].append(d)

    return 0
    
#--------------------
# sum_shared_data
# i : index
#--------------------
def sum_shared_data(i):
    global shared_data
    sum = 0
    for d in shared_data[i]:
        sum += d       
    return sum

#--------------------
# avg_shared_data
# i : index
#--------------------
def avg_shared_data(i):
    global shared_data
    sum = 0
    for d in shared_data[i]:
        sum += d
    
    sum = sum/len(shared_data[i])
    return sum
    
#--------------------
# dump_shared_data
# i : index
#--------------------
def dump_shared_data(i):
    global shared_data
    for d in shared_data[i]:
        print 'd:',d

#--------------------
# get_shared_data_len
# i : index
#--------------------
def get_shared_data_len(i):
    global shared_data
    return len(shared_data[i])
        
#--------------------
# gen_rt_power
# i : source
# j : destination
# w : width
#--------------------
def gen_rt_power(i,j,w):
    global shared_data
    d = shared_data[i][-1]
    d = d * 220/10000.0
    cache_shared_data(j,d,w)  
    return  d

  


#--------------------
# gen_rt_power_delta
# i : source
# j : destination
# w : width
#--------------------
def gen_rt_power_delta(i,j,w):
    global shared_data
    if len(shared_data[i]) < 2:
        return 0
        
    d = shared_data[i][-1] - shared_data[i][-2]
    cache_shared_data(j,d,w)  
    return  d
    
    
#--------------------
# readfile
#--------------------        
def readfile(filename):
    f = file(filename,'rb')
    fs = f.read()
    f.close()
    return fs

#--------------------
# writefile
#--------------------
def writefile(filename,content):
    agent_info('write file filename:'+filename)
    f = file(filename,'wb')
    fs = f.write(content)
    f.close()
    return

#--------------------
# has_file
#--------------------
def has_file(filename):
    if os.path.exists(filename):
        return True
    else:
        return False
 
#--------------------
# find_next_cfgfile
#--------------------
def find_next_cfgfile():
    while(1):
        print '.....'
        if (has_file('./config/config.idx')):
            f = readfile('./config/config.idx')
            current_cfg_f = f
                
            if (int(f[f.find('gateway.')+8]) + 1) >= 10:
                i = 0
            else:
                i = int(f[f.find('gateway.')+8]) + 1
                
            new_filename = './config/gateway.' + str(i) + '.cfg'
            if (has_file(new_filename)):
                writefile('./config/config.idx',new_filename)
                agent_info('select new available config file:' + new_filename)
            else:          
                writefile('./config/config.idx','./config/gateway.0.cfg')
                agent_info('select new available config file: gateway.0.cfg')

            if (has_file(current_cfg_f)):
                return current_cfg_f
            else:
                return new_filename
            
        else:
            writefile('./config/config.idx','./config/gateway.0.cfg')
            return './config/gateway.0.cfg'
        time.sleep(0.1)

#----------------------------------
# write_to_last_available_cfgfile
#----------------------------------
def write_to_last_available_cfgfile(f):
    for i in range(0,9):
        c = './config/gateway.%s.cfg' % (str(i))
        if not has_file(c):
            print 'write_to_last_available_cfgfile -- found available file name:',c
            c = writefile(c,f)
            return
        else:
            print 'write_to_last_available_cfgfile -- existed file name:',c
    c = './config/gateway.9.cfg'
    c = writefile(c,f)
    return
    
    
#----------------------------------
# write_sedona
#----------------------------------
def write_sedona(path,s):
    fname = './sedona/' + path
    c = writefile(fname,s)
    if (path.find('svm') >= 0):
        os.system('chmod 755 ' + fname)
    return 

 
#--------------------
# load_current_cfgfile
#--------------------
def load_current_cfgfile():
    if (has_file('./config/config.idx')):
        f = readfile('./config/config.idx')
        if (has_file(f)):
            return f
    writefile('./config/config.idx','./config/gateway.0.cfg')
    return './config/gateway.0.cfg'
            

#--------------------
# agent_logging_init
#--------------------
def agent_logging_init():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='agent.log',
                    filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

#--------------------
# agent_debug
#--------------------
def agent_debug(s):
    logging.debug(s)

#--------------------
# agent_info
#--------------------
def agent_info(s):
    logging.info(s)

#--------------------
# agent_warning
#--------------------
def agent_warn(s):
    logging.warning(s)

#--------------------
# read_json_from_file
#--------------------
def read_json_from_file(json_file):
    fin = open(json_file, 'r')
    cfg_dict = {}
    js = json.loads(fin.read())
    return js

#--------------------------
# remove_bin_block_header
#--------------------------
def remove_bin_block_header(pkg):
    if len(pkg) == 0:
        return pkg
    if pkg[0].encode('hex')[0:2] == '1b':
        n1 = pkg[0:20].find('\r\n')
        n2 = int(pkg[1:n1])
        #print 'n2:',n2
        pkg_removed_bin_header = pkg[n1+2:n1+2+n2]
        return pkg_removed_bin_header
    else:
        return pkg
        
#------------------------------
# split_with_bin_block_support
#------------------------------
def split_with_bin_block_support(pkg):
    new_blocks = []
    if len(pkg) == 0:
        return new_blocks
    off = 0
    last_off = 0
    loop = 1
    #print 'pkg type:',type(pkg)
    pkg_len = len(pkg)
    while (loop):
        off = pkg.find('\r\n', last_off)
        if (off != -1):     
            if (last_off == off):
                loop = 0
                return new_blocks
            #print '#off:',off,'#last_off',last_off,'#pkg_len:',pkg_len
            line = pkg[last_off:off]
            #print 'line(hex)',line.encode('hex')
            if line[0].encode('hex')[0:2] == '1b':
                bin_block_len = int(line[1:])
                last_off = off + 2 + bin_block_len
                bin_line = pkg[off+2:last_off]
                #print '++++++++++++++++1...line:'
                new_blocks.append(bin_line)
            else:
                #print '++++++++++++++++2...line:',line               
                new_blocks.append(line)
                last_off = off + 2
        else:
            loop = 0
            if (last_off < pkg_len):
                last_line = pkg[last_off:]
                #print '+++++++++++++++++3...line:',last_line                               
                new_blocks.append(last_line)
        if (last_off >= pkg_len):
            loop = 0
    #print 'new_blocks:',new_blocks
    return new_blocks
    
#-----------------------
# remove_aes_encryption
#-----------------------
def remove_aes_encryption(payload,aes_key):
    if payload[0:5] == 'ENC\r\n':
        #print 'before bin block removing: ',payload[5:].encode('hex')
        raw_cmd_encrypted = remove_bin_block_header(payload[5:])
        #print 'after bin block removing: ',raw_cmd_encrypted.encode('hex'), ',len:', len(raw_cmd_encrypted.encode('hex'))/2
        raw_cmd = aes256crypto.decrypt(raw_cmd_encrypted,aes_key)
        return 1, raw_cmd
    else:
        raw_cmd = payload
        return 0, raw_cmd
    
#-----------------------
# add_aes_encryption
#-----------------------    
def add_aes_encryption(raw_payload,aes_key):
    encrypted_payload = aes256crypto.encrypt(raw_payload,aes_key)
    lens = len(encrypted_payload)
    encrypted_payload_with_bin_block = 'ENC\r\n\x1b' + str(lens) + '\r\n' + encrypted_payload +'\r\n'
    #print 'add_aes_encryptiong: ',encrypted_payload_with_bin_block.encode('hex')
    return encrypted_payload_with_bin_block
    
#-----------------------
# sw_wdt_clear
#-----------------------    
def sw_wdt_clear():
    global wdt_timer
    wdt_timer = time.time()    

#-----------------------
# wdt_task
#-----------------------    
def wdt_task():
    global wdt_timer
    global mqtt_run_flag
    i = time.time() - wdt_timer
    #print 'wdt_task, time = ',i
    if (i >= 300):
        agent_warn('timeout, exit!')
        sys.exit(-1)
        return

#-----------------------
# check_app_status
#-----------------------    
def check_app_status(appname):
    try:
        f = '/tmp/' + appname + '.pid'    
        pid_str = readfile(f)
        os.system("ps -A | grep %s>%s"% (str(pid_str),'/tmp/ps_status'))
        os.system('cat /tmp/ps_status')
        if (os.path.getsize('/tmp/ps_status') < 6):
            return False
        else:
            return True
    except:
        return False

#-----------------------
# raw_to_configstring
#-----------------------         
def raw_to_configstring(s):
    s2 = s.replace('\n','')
    s2 = s2.replace('\r','\\n')
    s2 = s2.replace('"','\\"')
    s2 = '"' + s2 + '"'
    return s2

#-----------------------
# configstring_to_raw
#-----------------------     
def configstring_to_raw(s):
    s2 = s[1:-1]
    s2 = s2.replace('\\n','\r\n')
    s2 = s2.replace('\\"','"')
    return s2    

#------------------------------
# format_time_from_linuxtime
#------------------------------
def format_time_from_linuxtime(t):
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t)))
    return s
    
def get_linuxtime_from_string(s):
    struct_time = time.strptime(s,'%Y-%m-%d %H:%M:%S')
    t = time.mktime(struct_time)
    return t
    
#-------------------
# log_dump
#-------------------
def log_dump(filename,content):
    if os.name == "nt":
        fpath = '.\\filesystem\\log\\' + filename
    else:
        fpath = './filesystem/log/' + filename
    
    f = file(fpath,'ab')
    t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fs = f.write(t_s + '->' + str(content) + '\r\n')
    f.close()
    return

#-------------------
# kill_process
#-------------------
def kill_process(pid):
    if os.name == "nt":
        stop_cmd = 'taskkill /F /PID ' + pid
        os.system(stop_cmd)
    else:
        stop_cmd = 'kill ' + pid
        os.system(stop_cmd)
        
#-----------------------------
# mysendmail 
#
# p1: receiver
# p2: subject
# p3: content
#-----------------------------
def mysendmail(p1,p2,p3):
    global mail_enable
    global mail_sender,mail_smtpserver,mail_username,mail_password
    import sys,os
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    sender = mail_sender
    smtpserver = mail_smtpserver
    username = mail_username
    password = mail_password
    
    if (mail_enable == 0):
        return
    receiver=p1
    subject = p2
    if (len(p3) > 0):
        msg = MIMEText(p3,'plain','utf-8')
    else:
        msg = MIMEText('..','plain','utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # prepare attachment
    #att = MIMEText(open('h:\\python\\1.jpg', 'rb').read(), 'base64', 'utf-8')
    #att["Content-Type"] = 'application/octet-stream'
    #att["Content-Disposition"] = 'attachment; filename="1.jpg"'
    #msg.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print "mail sent!" 


#-------------------
# csv_save
#-------------------
def csv_save(filename,dp_name,data):
    try:
        t = time.time()
        filename2 = filename  
        if os.name == "nt":
            fpath = '.\\filesystem\\data\\' + filename2 + '.csv'
        else:
            fpath = './filesystem/data/' + filename2 + '.csv'
        
        #print 'fpath:',fpath
        f = file(fpath,'ab')
        #t = time.time()
        t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        #t_s = t_s + '%.3f' % (t%60)
        
        fs = f.write(t_s + ',' + str(t) + ',' + str(dp_name) + ',' + str(data) + '\r\n')
        f.close()
        return 0
    except:
        return -1

#-------------------
# csv_save2
#-------------------
def csv_save2(filename,dp_name,data):
    try:
        t = time.time()
        filename2 = time.strftime('%Y-%m-%d', time.localtime(t)) + '-' + filename  
        if os.name == "nt":
            fpath = '.\\filesystem\\data\\' + filename2 + '.csv'
        else:
            fpath = './filesystem/data/' + filename2 + '.csv'
        
        #print 'fpath:',fpath
        f = file(fpath,'ab')
        #t = time.time()
        t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        #t_s = t_s + '%.3f' % (t%60)
        
        fs = f.write(t_s + ',' + str(t) + ',' + str(dp_name) + ',' + str(data) + '\r\n')
        f.close()
        return 0
    except:
        return -1
        
#-------------------------------------
# get_future_price
#-------------------------------------
def get_future_price(future_name='AG1512'):
    try:
        url = "http://hq.sinajs.cn/?_=%s/&list=%s" %(str(time.time()*1000),future_name)
        #url = "http://hq.sinajs.cn/&list=%s" %(future_name)
        #print 'get_future_price url:',url
        f = urllib2.urlopen(url)
        s = f.read()
        print s
        f.close()

        if (s.find('var') != 0):
            #print 'get_future_price --- error!'
            return -2,0
        else:
            s3 = s.split(',')
            #print s3
            if float(s3[8]) == 0:
                return -3, float(s3[8])
            else:
                return 0, float(s3[8])
            
    except:
        return -1,0

#----------------------
# iot_data_svr_save_data
#----------------------
def iot_data_svr_save_data(ip,port,key,id,value):
    try:
        rpc_handler = pyiotlib.app_sdk(key,server_ip=ip,server_port=port)
        json_out = rpc_handler.save_data(str(id),str(value))
        if json_out['code'] < 0:
            print 'error:',json_out['data']
            return -1
        else:
            print 'id:%s, value:%s' % (str(id),str(value))
            return 0
    except:
        print 'iot_data_svr_save_data exception'
        return -2
        
#--------------------------------------------
# main -- unittest
#--------------------------------------------
if __name__ == '__main__':
    cache_shared_data(0,10000,5)
    gen_rt_power(0,1,5)
    gen_rt_power_delta(1,2,5)
    
    cache_shared_data(0,12000,5)
    gen_rt_power(0,1,5)
    gen_rt_power_delta(1,2,5)
    
    cache_shared_data(0,10000,5)
    gen_rt_power(0,1,5)
    gen_rt_power_delta(1,2,5)
    
    cache_shared_data(0,10000,5)
    gen_rt_power(0,1,5)
    gen_rt_power_delta(1,2,5)
    
    cache_shared_data(0,10000,5)
    gen_rt_power(0,1,5)
    gen_rt_power_delta(1,2,5)
    
    print 'raw_data:'
    dump_shared_data(0)
    
    print 'rt_power:'
    dump_shared_data(1)

    print 'rt_power_delta:'
    dump_shared_data(2)
    
    retcode,p = get_future_price('AG1701')
    print retcode,p
    csv_save('test','i',345.4);
    csv_save2('test','i',345.4);
    s = raw_input()
    

    
    
        