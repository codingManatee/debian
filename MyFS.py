#!/usr/bin/env python3

# 2110352 Operating System
# FUSE/Filesystem exercise
# By Krerk Piromsopa, Ph.D. <Krerk.P@chula.ac.th>
#    Department of Computer Engineering
#    Chulalongkorn University.

import os, stat, errno
import fuse
from fuse import Fuse
import requests

if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-py doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)

containers={ \
            '/subject':b"2018S1 - Operating Systems\nCP ENG CU\n",
            '/instructors': b"0:CP ENG CU OS 2018S1 - Instructors\n1:    Thongchai Rojkandsadan\n2:    Veera Muangsin, Ph.D.\n3:    Krerk Piromsopa, Ph.D.\n",
            '/students': b"0:CP ENG CU OS 2018S1 - Students, Group Name: fbb\n1:    6430222521 Pattapon Vichanukroh \n2:    6431331421 Punnawich Yiamsombat \n",
            '/participation': b""
            }

def myRead():
    req=requests.get('https://mis.cp.eng.chula.ac.th/krerk/teaching/2022s2-os/status.php')
    content = bytes(req.text, 'utf-8')
    return content

def myWrite(buf):
    decoded_buf = buf.decode('utf-8')
    raw=decoded_buf.split(':')
    checkInUrl='https://mis.cp.eng.chula.ac.th/krerk/teaching/2022s2-os/checkIn.php'
    params={'studentid': raw[0], 'name': raw[1], 'email': raw[2]}
    rpost = requests.post(checkInUrl, data=params)
    return len(buf)

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 1000
        self.st_gid = 1000
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class MyFS(Fuse):

    def getattr(self, path):
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0o0777
            st.st_nlink = 2
        elif path in containers:
            st.st_mode = stat.S_IFREG | 0o0444
            st.st_nlink = 1
            if path == '/participation':
                st.st_mode = stat.S_IFREG | 0o0666
                content=myRead()
            else:
                content=containers[path]
            st.st_size = len(content)
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        filenames=containers.keys()
        for r in  '.', '..':
            yield fuse.Direntry(r)


        for r in filenames:
            yield fuse.Direntry(r[1:])

    def open(self, path, flags):
        if path not in containers:
            return -errno.ENOENT

    def read(self, path, size, offset):
        if path not in containers:
            return -errno.ENOENT

        if path=='/participation':
            content = myRead()
        else:
            content = containers[path]

        slen = len(content)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = content[offset:offset+size]
        else:
            buf = ''
        return buf
    def write(self, path, buf, offset):
        if path=='/participation':
            return myWrite(buf)

        return -errno.ENOENT

def main():
    usage="""
MyFS mounting_point

""" + Fuse.fusage
    server = MyFS(version="%prog " + fuse.__version__,
                  usage=usage,
                  dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
