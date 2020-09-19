import subprocess
import re

class Conf:
  remoteHost = 'selenium-chrome'
  remoteServer = 'http://' + remoteHost + ':4444/wd/hub'
  interval  = 2

  dirBase = '/app/'
  dirResource = f'{dirBase}static/'

  dirImage = '%simages/' % dirResource
  dirCss = '%scss/' % dirResource

  dirStorage =  f'{dirResource}storage/'
  dirSS = f'{dirStorage}screenShot/'
  dirCsv = f'{dirStorage}csv/'

  def getAbsolutePath(relPath: str):
    return Conf.dirBase + relPath

  def getDockerHostUtl()-> str:
    output = subprocess.check_output("ip route | awk 'NR==1 {print $3}'", shell=True)
    return 'http://' + re.findall('\d+\.\d+\.\d+\.\d+', output.decode('utf8'))[0]
