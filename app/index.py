from flask import Flask, render_template

from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen
from modules.sites.testSite.pages import *
#from modules.sites.tso_bus.pages import *
from modules.conf import Conf
from modules.Analizer import Analizer

from pprint import pprint
import traceback
import time
import random
import json

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/google')
def google():
  driver = getChromeDriver()
  page = GooglePage(driver)
  return test(driver, page)

@app.route('/select')
def select():
  driver = getChromeDriver()
  page = QuickRefSelectPage(driver)
  return test(driver, page)

@app.route('/radio')
def radio():
  driver = getChromeDriver()
  page = QuickRefRadioPage(driver)
  return test(driver, page)

@app.route('/checkbox')
def checkbox():
  driver = getChromeDriver()
  page = QuickRefCheckboxPage(driver)
  return test(driver, page)

@app.route('/label')
def label():
  driver = getChromeDriver()
  page = QuickRefLabelPage(driver)
  return test(driver, page)

@app.route('/shinro')
def shinro():
  driver = getChromeDriver()
  page = DocsApplyPage(driver)
  return test(driver, page)

#@app.route('/bus')
#def bus():
#  driver = getChromeDriver()
#  #driver = getChromeHeadlessDriver()
#
#  page = TsoApplyPage(driver)
#  return test(driver, page)

def test(driver, page):
  try:
    page.test()

    testResult = 'success'
    error = ''
  except Exception as e:
    testResult = 'failure'
    error = traceback.format_exc()
  finally:
    image = '%s.png' % (testResult)
    time.sleep(3) # wait for page transition
    fullScreen(driver)
    screenShot(driver, testResult)

    driver.close()
    driver.quit()
    randamInt = random.randrange(1, 65535)
    return render_template('test.html', error = error, image = image, randamInt = randamInt)

@app.route('/analizer')
def analizer():
  #url = "https://google.com"
  url = "https://qiita.com/yoshi0518/items/14690172f41c32c8286b"
  driver = getChromeDriver()
  try:
    analizer = Analizer(url, driver)
    data = analizer.getLinks()
    error = ''
  except Exception as e:
    data = {}
    error = traceback.format_exc()
  finally:
    driver.close()
    driver.quit()
    return render_template('analizer.html', data = data, error = error)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=80)