from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from .driver import screenShot, screenShotFull
from selenium.webdriver.common.by import By

"""visit https://selenium-python.readthedocs.io/page-objects.html for more info"""

WD = 5

class ElementBase:
  waitDuration = WD
  def __init__(self, locator: tuple):
    self.locator = locator

  def getElement(self, driver, locator):
    WebDriverWait(driver, self.waitDuration).until(
        lambda driver: driver.find_element(*locator))
    return driver.find_element(*locator)
class FormTextElement(ElementBase):
  waitDuration = WD
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//input[@type="text"][@name="' + name + '"]')

  def __get__(self, obj, owner):
    locator = self.locator
    element = self.getElement(obj.driver, locator)
    return element.get_attribute("value")

  def __set__(self, obj, value):
    locator = self.locator
    element = self.getElement(obj.driver, locator)
    element.clear()
    element.send_keys(value)

class FormSelectElement(ElementBase):
  waitDuration = WD
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//select[@name="' + name + '"]')

  def __get__(self, obj, owner):
    locator = self.locator
    element = self.getElement(obj.driver, locator)
    return element.get_attribute("value")

  def __set__(self, obj, value: tuple):
    by = str(value[0])
    key = value[1]

    locator = self.locator
    element = self.getElement(obj.driver, locator)
    select = Select(element)
    options = select.options

    if (by == 'index'):
      if not isinstance(key, int): raise Exception('arg2 expects int type but received ' + key)
      select.select_by_index(key)
    elif (by == 'value'):
      select.select_by_value(str(key))
    elif (by == 'text'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + key)
      select.select_by_visible_text(str(key))
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

class FormRadioElements(ElementBase):
  waitDuration = WD
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//input[@type="radio"][@name="' + name + '"]')

  def __get__(self, obj, owner):
    locator = self.locator
    elements = obj.driver.find_elements(*locator)
    for element in elements:
      if element.is_selected():
        elemSelected = element
        break
    return elemSelected.get_attribute("value")

  def __set__(self, obj, value: str):
    xpath = self.locator[1]
    xpath += '[@value="' + value + '"]'
    locator = (self.locator[0], xpath)
    element = self.getElement(obj.driver, locator)
    element.click()

class FormCheckboxElement(ElementBase):
  waitDuration = WD
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//*[@type="checkbox"][@name="' + name + '"]')

  def __get__(self, obj, owner):
    locator = self.locator
    return self.getElement(obj.driver, locator)

  def __set__(self, obj, value: tuple):
    target = str(value[0])
    action = str(value[1])

    xpath = self.locator[1]
    xpath += '[@value="' + target + '"]'
    locator = (self.locator[0], xpath)
    element = self.getElement(obj.driver, locator)

    state = element.is_selected()

    if (action == 'toggle'):
      element.click()
    elif (action == 'check'):
      if not state: element.click()
    elif (action == 'uncheck'):
      if state: element.click()
    else:
      raise Exception('invalid action ' + action  + ' for ' + __class__.__name__)

class FormSubmitElement(ElementBase):
  waitDuration = WD
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//*[@name="' + name + '"]')

  def __get__(self, obj, owner):
    locator = self.locator
    return self.getElement(obj.driver, locator)