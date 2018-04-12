#!/usr/bin/python

import unittest

import sys
if '..' not in sys.path:
    sys.path.append('..')
    from dataupload import NLSDataUpload

if __name__=='__main__':

    nlsdataupload = NLSDataUpload('10.129.113.142','root','nls72NSN', debug=True)
    if nlsdataupload.login():
        print('login successfully')
    else:
        print('login Failed')

    if nlsdataupload.uploadLTEBSData(f='../data/ltelaxu.csv'):
        print('Upload File Successfully!')
    else:
        print('Upload Failed!')
    ###

    spdata= {
            'save':'save',
            'userid':'laxu'+nlsdataupload.csrftoken[0:5],
            'password':'111',
            'privatelevel':'1',
            'flownumber':'2',
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

    if nlsdataupload.addSP(spdata):
        print('Add SP Basic Info successfully!')
    else:
        print('Add SP Basic Info Failed!')


