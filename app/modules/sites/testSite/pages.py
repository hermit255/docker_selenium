from ...page import *
from modules.driver import screenShot, screenShotFull

import time
from selenium.webdriver.common.by import By

class GooglePage:
  search = FormTextElement('q')
  sButton = FormSubmitElement('btnK')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://google.com'
    self.driver.get(url)
    self.search = 'dog'
    self.sButton.submit()

class QuickRefSelectPage:
  bloodSelect = FormSelectElement('blood')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/select.shtml'
    self.driver.get(url)
    self.bloodSelect = ('text', 'AB型')

class QuickRefRadioPage:
  radios = FormRadioElements('hyouka')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_radio.shtml'
    self.driver.get(url)
    #self.radios = 'bad'
    self.radios = 'good'

class QuickRefCheckboxPage:
  checkbox = FormCheckboxElement('riyu')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'http://www.htmq.com/html/input_checkbox.shtml'
    self.driver.get(url)
    self.checkbox = (1, 'toggle')
    self.checkbox = (2, 'check')
    self.checkbox = (3, 'check')



class XPage:
  #first = ElementBase(('text', '大学'))
  first = ElementBase(('xpath', '//label[@for="D"]'))
  bunya = FormCheckboxElement('bunya[110]')
  areaB = FormCheckboxElement('hopeAreaB[]')
  button = FormSubmitElement('all')

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://shinronavi.com/omakase/select'
    self.driver.get(url)
    self.first.getElement(self.driver, self.first.locator).click()
    self.bunya = (1, 'toggle')
    self.areaB = (2, 'toggle')
    self.areaB = (3, 'toggle')
    self.areaB = (40, 'toggle')
    self.button.click()