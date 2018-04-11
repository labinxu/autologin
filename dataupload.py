#!/bin/env python

import utils,os
from utils import util_requests
import optparse, md5
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def commandline():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--username', dest="username", default='root', help="user name")
    parser.add_option('-p', '--password', dest="password", default='nls72NSN', help="password")
    parser.add_option('-l', '--lte', dest="ltedata", default="./data/ltelaxu.csv", help="LTE BS data file")
    parser.add_option('-s', '--server', dest="server", default="10.129.113.142", help="NLS vnl server ip")
    return parser.parse_args()

class NLSDataUpload():
    def __init__(self, server, username, password, debug=False):
        self.username = username
        self.debug = debug
        m1 = md5.new()
        m1.update(password)
        self.password = m1.hexdigest()
        self.password_i = '*'*len(password)

        self.requester = util_requests.UtilityRequests(domain='')
        self.server = server
        self.url_index = 'mals60_term/go_index.do'
        self.url_nlshome = 'mals60_term/NLSHome.do'

    def _make_url(self, page):
        url = 'http://{server}:8080/{page}'.format(server=self.server, page=page)
        logger.info(url)
        return url

    def login(self):
        loginurl = self._make_url(self.url_index)
        s = self.requester.getSoup(loginurl)

        # CSRFTOKEN
        tokentag = s.find('input', attrs={'name':'CSRFTOKEN'})
        self.csrftoken = tokentag['value']
        logger.debug(self.csrftoken)

        playdata = {'CSRFTOKEN': tokentag['value'],
                    'txt_popupwindowvalue': '0',
                    'languageSelect': 'English',
                    'username': self.username,
                    'password': self.password,
                    'password_i': self.password_i}

        logger.debug(str(playdata))
        urlhome = self._make_url(self.url_nlshome)
        resp = self.requester.post(urlhome, data=playdata)
        if self.debug:
            with open('/home/laxxu/login.html','w') as f:
                f.write(resp.text)
        return True if resp.text.find('Sorry') == -1 else False

    def addSP(self, data):
        addsp = 'mals60_term/aspsa/asps102?CSRFTOKEN=%s' % self.csrftoken
        url = self._make_url(addsp)
        if data:
            resp = self.requester.post(url, data=data)
            import pdb;pdb.set_trace()
            return resp.text.find('Add SP Basic Info successfully') == 1
        return False

    def uploadLTEBSData(self, f):
        from requests_toolbelt import MultipartEncoder
        logger.info('upload %s' %f)
        ct = 'application/octet-stream'
        page = 'mals60_term/absaa/absa102?CSRFTOKEN=%s' % self.csrftoken
        url_LTEdata = self._make_url(page)

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
        if self.debug:
            with open('/home/laxxu/uploadlete.html', 'w') as f:
                f.write(resp.text)
        return True if resp.text.find('Upload File successfully') != -1 else False

def main():
    opt, var = commandline()
    nlsdataupload = NLSDataUpload(server=opt.server,
                                  username=opt.username,
                                  password=opt.password,
                                  debug=True)
    if not nlsdataupload.login():
        logger.error('Login failed!')
        return
    logger.info('Login Successful!')
    if nlsdataupload.uploadLTEBSData(f=opt.ltedata):
        logger.info('Upload File Successfully!')
    else:
        logger.error('Upload Failed!')

    jsondata = {
        "save":"save","userid":"1111","password":"1111","privatelevel":"1","flownumber":"100",
        "maxnumber":"10",
        "vaildtime":"2020-12-31",
        "activeflag":"1",
        "version":"10",
        "delineation":"description",
        "xydisplay":"0",
        "ipauthentication":"1",
        "coarselocationmark":"1",
        "CSRFTOKEN":nlsdataupload.csrftoken
    }

    if nlsdataupload.addSP(jsondata):
        logger.info('Add SP Basic Info successfully!')
    else:
        logger.error('Add SP Basic Info Failed!')

if __name__ == '__main__':
    main()
