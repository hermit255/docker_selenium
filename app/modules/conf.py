class Conf:
  remoteHost = 'selenium-chrome'
  remoteServer = 'http://' + remoteHost + ':4444/wd/hub'
  interval  = 2

  dirBase = '/app/'
  dirStorage =  '%sstorage/' % dirBase
  dirScreenShot = '%sscreenShot/' % dirStorage
  dirCsv = '%scsv/' % dirStorage

  dirResource = '%sstatic/' % dirBase
  dirImage = '%simages/' % dirResource