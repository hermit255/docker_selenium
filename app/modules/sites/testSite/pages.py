from ...page import *

import time
from selenium.webdriver.common.by import By

class GooglePage:
  search = FormText('q')
  sButton = ElementBase('//input[@value="Google 検索"]')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://google.com'
    self.driver.get(url)
    self.search = 'dog'
    self.sButton

class QuickRefSelectPage:
  bloodSelect = FormSelect('blood')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/select.shtml'
    self.driver.get(url)
    self.bloodSelect = ('index', 0)
    self.bloodSelect = ('value', 'B')
    self.bloodSelect = ('text', 'AB型')

class QuickRefRadioPage:
  radios = FormRadio('hyouka')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_radio.shtml'
    self.driver.get(url)
    self.radios = ('index', 1)
    self.radios = ('value', 'good')
    self.radios = ('value', 'bad')

class QuickRefCheckboxPage:
  checkbox = FormCheckbox('riyu')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_checkbox.shtml'
    self.driver.get(url)
    self.checkbox = ('index', 0, 'uncheck')
    self.checkbox = ('value', '2', 'check')
    self.checkbox = ('index', 2, 'toggle')

class QuickRefLabelPage(PageBase):
  sexRadio = FormRadio('sex')
  bloodRadio = FormRadio('blood')

  def test(self):
    url = 'http://www.htmq.com/html/label.shtml'
    self.driver.get(url)
    self.sexRadio = ('label', "女")
    self.bloodRadio = ('label', "O型")

class DocsApplyPage:
  first = ElementBase('//*[.="大学"]')
  bunya = FormCheckbox('bunya[110]')
  areaB = FormCheckbox('hopeAreaB[]')
  logo = LinkImage('/new/_app/_webroot/img/module/layout/logo_top.png')
  memberInfo = LinkText('会員情報呼びだし')
  goNext = ElementBase('//input[@name="all"]')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://shinronavi.com/omakase/select'
    self.driver.get(url)
    #self.logo.click()
    #self.memberInfo.click()
    self.first
    self.bunya = ('index', 0, 'toggle')
    self.areaB = ('index', 1, 'toggle')
    self.areaB = ('index', 2, 'toggle')
    self.areaB = ('index', 40, 'toggle')
    #self.goNext