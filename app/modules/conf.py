class Conf:
  remoteHost = 'selenium-chrome'
  remoteServer = 'http://' + remoteHost + ':4444/wd/hub'
  interval  = 2

  dirBase = '/app/'
  dirResource = '%sstatic/' % dirBase

  dirImage = '%simages/' % dirResource
  dirCss = '%scss/' % dirResource

  dirStorage =  '%sstorage/' % dirResource
  dirSS = '%sscreenShot/' % dirStorage
  dirCsv = '%scsv/' % dirStorage