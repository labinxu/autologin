#!/bin/env python
import utils,os
from utils import util_requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseLogin():
    def __init__(self, securetype='http', port='80', domain=''):
        self.username = ''
        self.password = ''
        self.csrftoken = ''
        self.requester = util_requests.UtilityRequests(domain=domain)
        self.server = ''
        self.securetype = securetype
        self.port = port

    def set_port(self, port):
        assert(port)
        self.port = port

    def set_secure(self,insecure=True):
        if insecure:
            self.securetype = 'http'
        else:
            self.securetype = 'https'

    def make_url(self, server, page):
        url = '{ttype}://{server}:{port}/{page}'.format(ttype=self.securetype, server=server, port=self.port, page=page)
        logger.debug(url)
        return url

    def login(self, loginpage, playdata=None):
        resp = self.requester.postSoup(loginpage, data=playdata)
        status = False if resp.find('font',text='WiFi Password.') else True
        if not status:
            logger.error('Login Failed')
            with open('./loginerror.html','w') as f:
                f.write(resp.text)

        return status, resp


    def _addreferer(self):
        referer = 'mals60_term/aspsa/asps101?CSRFTOKEN=%s'% self.csrftoken
        referer = self._make_url(self.server, referer)
        header  = {'Referer':referer}
        self.requester.addHeaders(header)
    def _postwithstatus(self, url, data):
        
        pass

    def addSP(self, data):
        self._addreferer()
        addsp = 'mals60_term/aspsa/asps102?CSRFTOKEN=%s' % self.csrftoken
        url = self._make_url(self.server, addsp)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.requester.addHeaders(header)
        status = False
        if data:
            data['CSRFTOKEN'] = self.csrftoken
            resp = self.requester.postSoup(url, data=data)
            status = True if resp.find('td',text='Add SP Basic Info successfully') else False
            if not status:
                logger.error(resp.text.replace(' ','').replace('\r\n','').replace('\n',''))
        return status
    
    def addAppID(self, data):
        self._addreferer()
        addappid = 'mals60_term/aspsa/aspsd02?CSRFTOKEN=%s'%self.csrftoken
        url = self._make_url(self.server, addappid)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.requester.addHeaders(header)
        status = False
        if data:
            data['CSRFTOKEN'] = self.csrftoken
            resp = self.requester.postSoup(url, data=data)
            status = True if resp.find('td', text='Add SET Application ID successfully') else False
            if not status:
                logger.error(resp.text.replace(' ','').replace('\r\n','').replace('\n',''))
                #return resp.text.find('Add SET Application ID successfully') != -1

        return status


    def uploadLTEBSData(self, f):
        from requests_toolbelt import MultipartEncoder
        logger.info('upload %s' %f)
        ct = 'application/octet-stream'
        page = 'mals60_term/absaa/absa102?CSRFTOKEN=%s' % self.csrftoken
        url_LTEdata = self._make_url(self.server, page)

        fields=(
            ('selectID','6'),
            ('file1', (os.path.basename(f), open(f, 'rb'), 'application/vnd.ms-excel')),
            ('file2',('',None, ct)),
            ('file3',('',None, ct)),
            ('isOper','no'),
            ('CSRFTOKEN',self.csrftoken)
        )

        m = MultipartEncoder(fields)
        self.requester.addHeaders({'Upgrade-Insecure-Requests':"1"})
        self.requester.addHeaders({'Content-Type':m.content_type})
        resp = self.requester.post(url_LTEdata, data=m)
        status = True if resp.text.find('Upload File successfully') != -1 else False
        if not status:
            with open('./uploadlete.html', 'w') as f:
                f.write(resp.text)
        return status
