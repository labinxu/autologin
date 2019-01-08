#!/usr/bin/python

"""
get data from web and dispatcher it
"""
import sys
sys.path.append('C:/msys64/usr/lib/python3.6/site-packages')

import os,  logging
#from requests_toolbelt import MultipartEncoder
from utils import util_requests
from commandline import CMDBuilder, cmdbuild
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@cmdbuild('wfdsp')
class PwdDisp(object):
    def __init__(self):
        pass

    @CMDBuilder.Args('-u','--username', default='laibin.xu', help='username')
    @CMDBuilder.Args('-p','--password', default='Jan@0101', help='password')
    @CMDBuilder.Args('-s', '--server', default='10.99.4.93', help='server')
    @CMDBuilder.Args('-e', '--email', default='laibin.xu@cienet.com.cn', help='user.email')
    @CMDBuilder.Args('-d', '--destemail', default='laibin.xu@cienet.com.cn', help='to email')
    @CMDBuilder.Args('-P', '--epwd', default='January@', help='email password')
    def showifi(self, username, password, server, email, destemail, epwd):
        from utils import baselogin
        bl = baselogin.BaseLogin()
        pd = {'name': username,
            'password': password,
            'submit': 'Submit'}
        _, resp = bl.login(bl.make_url(server , 'WifiCode/ldapauth.php'), pd)
        from utils import util_smtp
        destemail = destemail.split(',')
        print(destemail)
        email = util_smtp.util_smtp( email, destemail, epwd)
        email.send('wifi', resp.text)

if __name__=='__main__':
    CMDBuilder.run()
#itchat
