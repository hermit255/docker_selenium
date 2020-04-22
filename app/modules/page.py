from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from .driver import screenShot, screenShotFull

"""visit https://selenium-python.readthedocs.io/page-objects.html for more info"""

WD = 100

class ElementBase:
  def __init__(self, locator: tuple):
    self.locator = locator

  def getElement(self, driver):
    WebDriverWait(driver, self.waitDuration).until(
        lambda driver: driver.find_element(*self.locator))
    return driver.find_element(*self.locator)

class FormTextElement(ElementBase):
  waitDuration = WD
  def __set__(self, obj, value):
    element = self.getElement(obj.driver)
    element.clear()
    element.send_keys(value)
  def __get__(self, obj, owner):
    element = self.getElement(obj.driver)
    return element.get_attribute("value")

class FormSelectElement(ElementBase):
  waitDuration = WD
  def __set__(self, obj, value):
    element = self.getElement(obj.driver)
    select = Select(element)
    options = select.options
    by = value[0]
    key = value[1]
    if (by == 'index'):
      if not isinstance(key, int): raise Exception('arg2 expects int type but received ' + key)
      select.select_by_index(key)
    elif (by == 'value'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + key)
      select.select_by_value(key)
    elif (by == 'text'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + key)
      select.select_by_visible_text(key)
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

  def __get__(self, obj, owner):
    element = self.getElement(obj.driver)
    return element.get_attribute("value")

class FormSubmitElement(ElementBase):
  waitDuration = WD
  def __get__(self, obj, owner):
    return self.getElement(obj.driver)