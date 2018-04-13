#!/bin/env python

import utils,os
from utils import util_requests
import optparse, md5
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NLSDataUpload():
    def __init__(self):
        self.username = ''
        self.password = ''
        self.csrftoken = ''
        self.requester = util_requests.UtilityRequests(domain='')
        self.server = ''
        self.url_index = 'mals60_term/go_index.do'
        self.url_nlshome = 'mals60_term/NLSHome.do'

    def _make_url(self, server, page):
        url = 'http://{server}:8080/{page}'.format(server=server, page=page)
        logger.debug(url)
        return url

    def login(self, username, password, server):
        loginurl = self._make_url(server, self.url_index)
        s = self.requester.getSoup(loginurl)

        # CSRFTOKEN
        tokentag = s.find('input', attrs={'name':'CSRFTOKEN'})
        self.csrftoken = tokentag['value']
        self.username = username
        self.password = password
        self.server = server

        logger.debug(self.csrftoken)
        m = md5.new()
        m.update(password)

        playdata = {'CSRFTOKEN': tokentag['value'],
                    'txt_popupwindowvalue': '0',
                    'languageSelect': 'English',
                    'username': self.username,
                    'password': m.hexdigest(),
                    'password_i': '*'*len(password)
        }

        logger.debug(str(playdata))
        urlhome = self._make_url(server, self.url_nlshome)
        resp = self.requester.postSoup(urlhome, data=playdata)

        status = False if resp.find('font',text='Incorrect user or password.') else True
        
        # #status =  True if resp.text.find('Sorry') == -1 else False
        
        if not status:
            logger.error('Login Failed')
        #     with open('./loginerror.html','w') as f:
        #         f.write(resp.text)

        return status


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
        if data:
            data['CSRFTOKEN'] = self.csrftoke
            resp = self.requester.post(url, data=data)
            return resp.text.find('Add SET Application ID successfully') != -1

        return False


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
