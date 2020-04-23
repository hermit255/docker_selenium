from ...page import *
from modules.driver import screenShot, screenShotFull

import time
from selenium.webdriver.common.by import By

class GooglePage:
  search = FormText('q')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://google.com'
    self.driver.get(url)
    self.search = 'dog'
    self.sButton.submit()

class QuickRefSelectPage:
  bloodSelect = FormSelect('blood')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/select.shtml'
    self.driver.get(url)
    self.bloodSelect = ('text', 'AB型')

class QuickRefRadioPage:
  radios = FormRadios('hyouka')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_radio.shtml'
    self.driver.get(url)
    #self.radios = 'bad'
    self.radios = 'good'

class QuickRefCheckboxPage:
  checkbox = FormCheckbox('riyu')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_checkbox.shtml'
    self.driver.get(url)
    self.checkbox = (1, 'toggle')
    self.checkbox = (2, 'check')
    self.checkbox = (3, 'check')



class XPage:
  first = Label('大学')
  bunya = FormCheckbox('bunya[110]')
  areaB = FormCheckbox('hopeAreaB[]')
  logo = LinkImage('/new/_app/_webroot/img/module/layout/logo_top.png')
  memberInfo = LinkText('会員情報呼びだし')


  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://shinronavi.com/omakase/select'
    self.driver.get(url)
    #self.logo.click()
    self.memberInfo.click()
    #self.first.click()
    #self.bunya = (1, 'toggle')
    #self.areaB = (2, 'toggle')
    #self.areaB = (3, 'toggle')
    #self.areaB = (40, 'toggle')
    #self.button.click()