#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import json
import urllib2
from multiprocessing import Pool
from ftplib import FTP

#ftp 服务器链接
def ftpconnect():
    ftp_server = 'ftp.ncdc.noaa.gov'
    http_server = 'www1.ncdc.noaa.gov'
    username = ''
    password = ''
    ftp=FTP()
    ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
    ftp.connect(ftp_server,21) #连接
    ftp.login(username,password) #登录，如果匿名登录则用空串代替即可
    return ftp

def fetch_and_save_filename_list(year):
    ftp = ftpconnect()
    path = data_path + str(year)
    filename_list = ftp.nlst(path)
    with open(str(year)+'.json', 'wb') as fli:
        fli.write(json.dumps(filename_list))
    ftp.quit()
    return filename_list

def load_filename_list(year):
    filename = str(year)+'.json'
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return json.loads(f.read())
    else:
        return fetch_and_save_filename_list(year)

def http_download(src, dest, rewrite=False):
    if rewrite or not os.path.exists(dest):
        with open (dest, 'wb') as fp:
            fp.write(urllib2.urlopen(src).read())

def http_download_1(src_dest):
    http_download(src_dest[0],src_dest[1])

def formate_src(base_url, filename):
    return base_url + filename

def formate_dest(base_dir, filename):
    return os.path.join(base_dir, filename)

def formate_src_dest(filename, base_dir, year):
    return (formate_src('http://www1.ncdc.noaa.gov', filename),
            formate_dest(base_dir,
                        str(year) + '/' + filename[-20:]))

if __name__=="__main__":
    start_year = int(sys.argv[1])
    end_year   = int(sys.argv[2])
    n   = int(sys.argv[4])
    base_dir = sys.argv[3]
    data_path = '/pub/data/noaa/'    

    year = start_year
    while year<=end_year:
        filename_list = load_filename_list(year)

        year_dir = base_dir +'/' + str(year)
        if not os.path.isdir(year_dir):
            os.makedirs(year_dir)
            
        p = Pool(n)
        process = map(lambda f: formate_src_dest(f, base_dir, year),
                filename_list)
        print(process[0])
        while True:
            try:
                p.map(http_download_1, process)
                break
            except:
                print("retry-------")

        year = year + 1
    #while True:
    #    try:
    #        downloads(start_year,end_year,filepath)
    #        break
    #    except:
    #        print("-----------------retry")



