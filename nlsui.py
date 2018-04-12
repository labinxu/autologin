#!/usr/bin/python

"""
NLS web site handler
"""

import os, md5, logging, requests
#from requests_toolbelt import MultipartEncoder
from utils import util_requests
from nlsauto import CMDBuilder,cmdbuild

@cmdbuild('nls')
class NLSUI(object):
    # def __new__(cls, *args, **kwargs):
    #     CMDBuilder.CATEGORIES={'v1' : cls}
    @CMDBuilder.Args('-u','--username', default='root', help='username')
    @CMDBuilder.Args('-p','--password', default='nls72NSN', help='password')
    def login(self, username, password):
        print("login: %s %s" %(username, password))

if __name__=='__main__':
    CMDBuilder.run()
