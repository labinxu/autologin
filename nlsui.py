#!/usr/bin/python

"""
NLS web site handler
"""

import os, md5, logging, requests
#from requests_toolbelt import MultipartEncoder
from utils import util_requests
from nlsinitializer import NLSDataUpload
from commandline import CMDBuilder, cmdbuild
import logging, json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@cmdbuild('nls')
class NLSUI(object):
    def __init__(self):
        self.nlsinitializer = NLSDataUpload()

    @CMDBuilder.Args('-u','--username', default='root', help='username')
    @CMDBuilder.Args('-p','--password', default='nls72NSN', help='password')
    @CMDBuilder.Args('-s', '--server', default='10.129.113.132', help='server')
    def login(self, username, password, server):
        return self.nlsinitializer.login(username, password, server)
    
    @CMDBuilder.Args('ltedata', help='lte bs ok data file')
    def initltebsdata(self, ltedata):
        return self.nlsinitializer.uploadLTEBSData(ltedata)

    @CMDBuilder.Args('spdata', help='sp data file')
    def initspdata(self, spdata):
        return self.nlsinitializer.addSP(spdata)

    @CMDBuilder.Args('appdata',help='appid data file')
    def initappdata(self, appdata):
        return self.nlsinitializer.addAppID(appdata)

    @CMDBuilder.Args('-u', '--username', default='root', help='username')
    @CMDBuilder.Args('-p', '--password', default='nls72NSN', help='password')
    @CMDBuilder.Args('-i', '--insecure', action="store_true", dest="insecure", help='insecure is http, else https')
    @CMDBuilder.Args('-s', '--server', default='10.129.113.132', help=' server ip')
    @CMDBuilder.Args('-l', '--ltedata', default='', help='the lte base data file type is csv')
    @CMDBuilder.Args('-S', '--spdata', default='', help='SP data file json')
    @CMDBuilder.Args('-a', '--appdata', default='', help='App ID data file json')
    def init(self, username, password, insecure, server, ltedata, spdata, appdata):
        self.nlsinitializer.set_secure(insecure)
        if self.login(username, password, server):
            logger.info('Login successfully')
        else:
            logger.error('Login failed')
        #
        if ltedata:
            if self.initltebsdata(ltedata):
                logger.info('LTE BS Data Upload successfully')
            else:
                logger.error('LTE BS Data Upload Failed!')

        ###########################################
        spdata
        payload = {}
        if spdata and os.path.exists(spdata):
            with open(spdata) as f:
                payload = json.load(f)

            if not payload:
                logger.error('The spdata read failed')
            else:
                if self.initspdata(payload):
                    logger.info('Add SP Data successfully')
                else:
                    logger.error('Add SP Data Failed!')

        #######appdata
        payload = {}
        
        if appdata and os.path.exists(appdata):
            with open(appdata) as f:
                payload = json.load(f)

            if not payload:
                logger.error('The appdata file read failed!')
            else:
                if self.initappdata(payload):
                    logger.info('Add Appdata successfully!')
                else:
                    logger.error('Add Appdata Failed!')

        #################
        
if __name__=='__main__':
    CMDBuilder.run()
