from flask import Flask, render_template, request, jsonify, Response

from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen
from modules.sites.testSite.pages import *
from modules.conf import Conf
from modules.Analizer import Analizer
from modules.xpath import Xpath

from pprint import pprint
import traceback
import time
import random
import json
from time import sleep
import cv2
import math
import io
import base64
import re
import pandas as pd

app = Flask(__name__)

""" operation """
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

"""
analizer
画面内の特定要素をリストアップする機能
"""
@app.route('/analizer')
def analizer():
  #url = "https://google.com"
  url = "https://inuwaka-blog.com"
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

@app.route('/api/crawler', methods=["GET", "POST"])
def crawler():
  """
    List urlList
    {
      "label": "{page_name(free)}",
      "url": "http://{url}"
    }
  """
  #host = request.form['url'] if ("url" in request.form) else "http://inuwaka-blog.com"
  host = request.form['url'] if ("url" in request.form) else "https://dev.tlsc.grooowth.co.jp"
  label = 'root'
  driver = getChromeDriver()
  data = {}
  error = ''
  urlList = []
  try:
    urlList = crawl(urlList, host, label, driver, host, 0)
  except Exception as e:
    error = traceback.format_exc()
    return jsonify({"error": error})
  finally:
    driver.close()
    driver.quit()

  return Response(
    pd.DataFrame(urlList).to_csv(encoding='utf-8'),
    mimetype="text/csv",
    headers={"Content-disposition":
    "attachment; filename=test.csv"})

  # return jsonify({"urlList": urlList, "error": error})

""" 初期URLリストおよびリストから派生したURLを巡回してリンク先リストを追加する """
def crawl(urlList: list, url: str, label: str, driver: object, host: str, level: int):
  updated = urlList
  if re.match('^/.*$', url):
    modifiedUrl = host + url
  else:
    modifiedUrl = url
  # 既存リストにないURLだけを既存リストに追加＋再帰的にリンク発掘
  exists = sum(1 for u in updated if u['url'] == modifiedUrl) > 0
  maxLevel = level > 4
  innerPage = re.match('^#.*$', modifiedUrl)
  externalSite = not re.match('^%s.*$' % host, modifiedUrl)
  if exists or maxLevel or innerPage or externalSite: return updated
  updated.append({"label": label, "url": modifiedUrl, "level": level})

  analizer = Analizer(driver, modifiedUrl)
  time.sleep(1)
  children = analizer.getLinks()
  # 取得したhrefと既存リストURLとの重複チェック
  for c in children:
    if 'href' in c["attrs"]: href = c["attrs"]["href"]
    text = c["text"]
    if  sum(1 for u in updated if u['url'] == href) == 0:
      updated = crawl(updated, href, text, driver, host, level + 1)
  return updated

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
      fullScreen(driver)
      sleep(5)
      """refered: https://qiita.com/happou/items/5b7072d145a974380787"""
      img_base64 = driver.get_screenshot_as_base64()
      img_data = base64.b64decode(img_base64)
      img_np = np.fromstring(img_data, np.uint8)
      wholeImg = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

      elements = driver.find_elements('xpath', xpath)
      ss = []
      marks = []
      for element in elements:
        if element.is_displayed() == False:
          print('skip invisible element')
          continue

        """画像リンクやラベル付きinputの領域をelementから判別しようとしたが、処理が重くなったのでxpathで調整する設計とする"""

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

        """refered: https://gist.github.com/gachiemchiep/52f3255a81c907461c2c7ced6ede367a"""
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

        marks.append({ 'xStart': xStart, 'yStart': yStart, 'xEnd': xEnd, 'yEnd': yEnd })

      img, text, org = wholeImg, url, (10,20)
      fotFace, fontScale, color, thickness, lineType = cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA
      cv2.putText(img, text, org, fotFace, fontScale , color, thickness, lineType )
      for i, mark in enumerate(marks):
        xStart, yStart, xEnd, yEnd = mark['xStart'], mark['yStart'], mark['xEnd'], mark['yEnd']
        # 囲み
        wholeImg = cv2.rectangle(wholeImg, (xStart, yStart), (xEnd, yEnd), (0, 0, 255), 3)

      for i, mark in enumerate(marks):
        xStart, yStart, xEnd, yEnd = mark['xStart'], mark['yStart'], mark['xEnd'], mark['yEnd']
        # ナンバリング
        radius = 8
        wholeImg = cv2.circle(wholeImg, ((xEnd + radius + 2), (yEnd - radius + 2)), radius, (64, 64, 64), (radius * 2))

        img, text, org = wholeImg, str(i + 1).zfill(2), (xEnd, yEnd)
        fotFace, fontScale, color, thickness, lineType = cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA
        cv2.putText(img, text, org, fotFace, fontScale , color, thickness, lineType )

      retval, buffer = cv2.imencode('.png', wholeImg)
      elem_bytes = np.array(buffer).tostring()
      b64E = base64.b64encode(elem_bytes).decode('utf-8')
      data['report'] = b64E

      data['ss'] = ss
    except Exception as e:
      error = traceback.format_exc()
    finally:
      driver.close()
      driver.quit()
  return render_template('capture.html', data = data, error = error, docker_host_url = docker_host_url, randamInt = random.randrange(1, 65535))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=80)

