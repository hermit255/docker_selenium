#!/usr/local/bin/python3
remoteHost = 'selenium-chrome'
remoteServer = 'http://' + remoteHost + ':4444/wd/hub'
interval  = 2

dirBase = '/app/'
dirStorage = dirBase + 'storage/'
dirScreenShot = dirStorage + 'screenShot/'
dirCsv = dirStorage + 'csv/'