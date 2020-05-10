from flask import Flask, render_template, request

from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen
from modules.sites.testSite.pages import *
from modules.conf import Conf
from modules.Analizer import Analizer

from pprint import pprint
import traceback
import time
import random
import json
from time import sleep
import cv2
import os
import math
import io
import base64
import numpy as np

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
    return render_template('test.html', error = error, image = image, randamInt = random.randrange(1, 65535))

@app.route('/analizer')
def analizer():
  #url = "https://google.com"
  url = "https://qiita.com/yoshi0518/items/14690172f41c32c8286b"
  driver = getChromeDriver()
  try:
    analizer = Analizer(driver, url)
    data = analizer.getLinks()
    error = ''
  except Exception as e:
    data = {}
    error = traceback.format_exc()
  finally:
    driver.close()
    driver.quit()
    return render_template('analizer.html', data = data, error = error)

@app.route('/capture', methods=["GET", "POST"])
def capture():
  # initialize vars
  data = {}
  error = ''
  docker_host_url = Conf.getDockerHostUtl()

  if request.method == 'POST':
    url, xpath, title = request.form['url'], request.form['xpath'], 'test'
    data['url'] = url
    data['xpath'] = xpath

    driver = getChromeDriver()
    #driver = getChromeHeadlessDriver()

    try:
      driver.get(url)
      sleep(3)
      fullScreen(driver)
      sleep(2)
      #refered: https://qiita.com/happou/items/5b7072d145a974380787
      img_base64 = driver.get_screenshot_as_base64()
      img_data = base64.b64decode(img_base64)
      img_np = np.fromstring(img_data, np.uint8)
      wholeImg = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

      elements = driver.find_elements('xpath', xpath)
      ss = []
      i = 1
      for element in elements:
        """todo: aならラップする画像、inputならリンクするラベルを対象エレメントに代える"""

        rect = element.rect
        xStart = math.floor(rect['x'])
        yStart = math.floor(rect['y'])
        xEnd = math.floor(rect['x'] + rect['width'])
        yEnd = math.floor(rect['y'] + rect['height'])

        elemImg = wholeImg[yStart:yEnd, xStart:xEnd]
        if elemImg is None or elemImg.shape[0] == 0 or elemImg.shape[1] < 10:
          print('OVER LIMIT')
          print(element.text)
          print(str(yStart) + ', ' + str(yEnd) + ', ' + str(xStart) + ', ' + str(xEnd))
          continue

        retval, buffer = cv2.imencode('.png', elemImg)
        elem_bytes = np.array(buffer).tostring()
        b64E = base64.b64encode(elem_bytes).decode('utf-8')

        # ファイルに保存していると不要ファイルが増えて煩わしかった
        #cv2.imwrite(destPath, elemImg)
        #with open(destPath, "rb") as image_file:
        #  b64E = base64.b64encode(image_file.read()).decode('utf-8')

        # バイナリストリームに保存するアイデアもあったがうまく動かせなかった
        #with io.BytesIO() as memory:
        #  cv2.imwrite(memory, elemImg)
        #  BinStE = memory.getvalue()
        #b64E = base64.b64encode(BinStE).decode('utf-8')

        ss.append(b64E)

      data['ss'] = ss
    except Exception as e:
      error = traceback.format_exc()
    finally:
      driver.close()
      driver.quit()
  return render_template('capture.html', data = data, error = error, docker_host_url = docker_host_url, randamInt = random.randrange(1, 65535))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=80)

