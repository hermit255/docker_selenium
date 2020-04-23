#!/usr/local/bin/python3
from modules.conf import dirBase, dirScreenShot, remoteServer, interval
from selenium import webdriver

import datetime
import os

def getChromeDriver():
  options = webdriver.ChromeOptions()
  driver = webdriver.Remote( command_executor=remoteServer, desired_capabilities=options.to_capabilities())

  wSize = {'width': 1920, 'height': 1080}
  driver.set_window_size(wSize['width'], wSize['height'])

  driver.implicitly_wait(interval)
  return driver

def getChromeHeadlessDriver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  driver = webdriver.Remote( command_executor=remoteServer, desired_capabilities=options.to_capabilities())

  wSize = {'width': 1920, 'height': 1080}
  driver.set_window_size(wSize['width'], wSize['height'])

  driver.implicitly_wait(interval)
  return driver

def screenShot(driver: webdriver, title: str = None, dirSub: str = ''):
  title = getDateTimeStr() if title is None else title

  body = driver.find_element_by_xpath('//body')
  body.screenshot(getFullPath(title, dirSub))
  print('screenShot exported:' + getFullPath(title, dirSub))

def fullScreen(driver: webdriver):
  body = driver.find_element_by_xpath('//body')
  windowSize = driver.get_window_size()
  windowSize['height'] = body.size['height']
  driver.set_window_size(windowSize['width'], windowSize['height'])

def getDateTimeStr():
  dt = datetime.datetime.today()
  return dt.strftime("%Y%m%d%H%M%S")

def getFullPath(title: str, dirSub: str = ''):
  dirBase = dirScreenShot
  directory = dirBase + dirSub

  if not os.path.exists(directory):
    os.makedirs(directory)

  return directory + title + '.png'