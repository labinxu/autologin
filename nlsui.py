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

    @CMDBuilder.Args('-u', '--username', default='root', help='username')
    @CMDBuilder.Args('-p', '--password', default='nls72NSN', help='password')
    @CMDBuilder.Args('-s', '--server', default='10.129.113.132', help=' server ip')
    @CMDBuilder.Args('-l', '--ltedata', default='', help='the lte base data file type is csv')
    @CMDBuilder.Args('-S', '--spdata', default='', help='SP data file')
    @CMDBuilder.Args('-a', '--appid', default='', help='App ID data file')
    def init(self, username, password, server, ltedata, spdata, appid):
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

        payload = {}
        if spdata and os.path.exists(spdata):
            import pdb; pdb.set_trace()
            with open(spdata) as f:
                payload = json.load(f)
            spdata= {                              
                'save':'save',              
                'userid':'laxu',            
                'password':'111',           
                'privatelevel':'1',         
                "vaildtime":"2020-12-31",   
                "activeflag":"1",           
                "version":"10",             
                "delineation":"description",
                "xydisplay":"0",            
                "ipauthentication":"1",     
                "coarselocationmark":"1",   
                "CSRFTOKEN":''
            }                                   

            if not payload:
                logger.error('The spdata read failed')
            else:
                if self.initspdata(payload):
                    logger.info('Add SP Data successfully')
                else:
                    logger.error('Add SP Data Failed!')
        payload = {}
        
if __name__=='__main__':
    CMDBuilder.run()
