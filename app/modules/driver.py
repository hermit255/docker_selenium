#!/usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import subprocess
import datetime
import os

remoteHost = 'selenium-chrome'
remoteServer = 'http://' + remoteHost + ':4444/wd/hub'

interval  = 2

def getDriver():
  # connection
  driver = webdriver.Remote( command_executor=remoteServer, desired_capabilities=DesiredCapabilities.CHROME)
  driver.implicitly_wait(interval)
  return driver

def screenShot(driver: webdriver, title: str = None):
  # get datetime for filename
  dt = datetime.datetime.today()
  dtstr = dt.strftime("%Y%m%d%H%M%S")
  # save screen shot image
  diretory = '/app/screenShot/'
  #diretory = '/app/screenShot/' + dtstr + '/'

  if title is None:
    title = driver.title
  fileName = title + '.png'
  if not os.path.exists(diretory):
    os.makedirs(diretory)
  fullPath = diretory + fileName
  driver.save_screenshot(fullPath)