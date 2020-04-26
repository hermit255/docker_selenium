from flask import Flask, render_template

from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen
from modules.sites.testSite.pages import *
from modules.conf import *

from pprint import pprint
import traceback
import time
import shutil

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/google')
def google():
  driver = getChromeDriver()
  page = GooglePage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)

@app.route('/select')
def select():
  driver = getChromeDriver()
  page = QuickRefSelectPage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)

@app.route('/radio')
def radio():
  driver = getChromeDriver()
  page = QuickRefRadioPage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)

@app.route('/checkbox')
def checkbox():
  driver = getChromeDriver()
  page = QuickRefCheckboxPage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)


@app.route('/shinro')
def shinro():
  driver = getChromeDriver()
  page = DocsApplyPage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)

@app.route('/xpage')
def xpage():
  driver = getChromeDriver()
  page = XPage(driver)

  result = test(driver, page)
  error = result['error']
  image = result['image']
  return render_template('test.html', error = error, image = image)

def test(driver, page):
  try:
    page.test()
    time.sleep(3) # wait for page transition

    fullScreen(driver)
    screenShot(driver, 'test')
    image = "test.png"
    shutil.copy2(dirScreenShot + "test.png", dirImage + image)
    error = ''
  except Exception as e:
    fullScreen(driver)
    screenShot(driver, 'failure')
    image = "failure.png"
    shutil.copy2(dirScreenShot + "failure.png", dirImage + image)
    error = traceback.format_exc()
  finally:
    driver.close()
    driver.quit()
    return {'error': error, 'image': image}

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=80)