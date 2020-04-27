#!/usr/local/bin/python3
from modules.conf import dirBase, dirScreenShot, remoteServer, interval
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import os

def getChromeDriver():
  options = webdriver.ChromeOptions()
  driver = webdriver.Remote( command_executor=remoteServer, desired_capabilities=options.to_capabilities())

  wSize = {1920, 1080}
  driver.set_window_size(*wSize)

  driver.implicitly_wait(interval)
  return driver

def getChromeHeadlessDriver():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless")
  driver = webdriver.Remote( command_executor=remoteServer, desired_capabilities=options.to_capabilities())

  wSize = {1920, 1080}
  driver.set_window_size(*wSize)

  driver.implicitly_wait(interval)
  return driver

def screenShot(driver: webdriver, title: str = None, dirSub: str = ''):
  title = getDateTimeStr() if title is None else title
  body = driver.find_element_by_xpath('//body')
  body.screenshot(getFullPath(title, dirSub))
  #driver.save_screenshot(getFullPath(title, dirSub))
  print('screenShot exported:' + getFullPath(title, dirSub))

def fullScreen(driver: webdriver):
  WebDriverWait(driver, 3).until(
    lambda driver: driver.find_element('xpath', '//html'))
  html = driver.find_element('xpath', '//html')
  windowSize = driver.get_window_size()
  windowSize['height'] = html.size['height']
  driver.set_window_size(windowSize['width'], windowSize['height'])

def setWindowSize(driver: webdriver, value: tuple):
  width = value[0]
  height = value[1]
  windowSize = driver.get_window_size()
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