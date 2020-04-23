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

class SimpleElement(ElementBase):
  def __init__(self, xpath: str):
    self.locator = (By.XPATH, xpath)

  def __get__(self, obj, owner):
    return self.getElement(obj.driver, self.locator)

class Clickable(ElementBase):
  def __init__(self, xpath: str):
    self.locator = (By.XPATH, xpath)

  def __get__(self, obj, owner):
    return self.getElement(obj.driver, self.locator)

  def __set__(self, obj, value):
    # クリックする
    # //div/li[a][%s]/a を想定するとして
    xpath = self.locator[1] % value
    locator = (self.locator[0], xpath)
    self.getElement(obj.driver, locator).click

class LinkText(ElementBase):
  def __init__(self, text: str):
    self.locator = (By.XPATH, '//a[.="' + text + '"]')

  def __get__(self, obj, owner):
    return self.getElement(obj.driver, self.locator)

class LinkImage(ElementBase):
  def __init__(self, src: str):
    self.locator = (By.XPATH, '//a[img[@src="' + src + '"]]')

  def __get__(self, obj, owner):
    return self.getElement(obj.driver, self.locator)

class Label(ElementBase):
  def __init__(self, text: str):
    self.locator = (By.XPATH, '//label[.="' + text + '"]')

  def __get__(self, obj, owner):
    return self.get(obj.driver, self.locator)

class FormText(ElementBase):
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//input[@type="text"][@name="' + name + '"]')

  def __get__(self, obj, owner):
    element = self.getElement(obj.driver, self.locator)
    return element.get_attribute("value")

  def __set__(self, obj, value):
    locator = self.locator
    element = self.getElement(obj.driver, locator)
    element.clear()
    element.send_keys(value)

class FormSelect(ElementBase):
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//select[@name="%s"]' % name)

  def __get__(self, obj, owner):
    element = self.getElement(obj.driver, self.locator)
    return element.get_attribute("value")

  def __set__(self, obj, value: tuple):
    by = str(value[0])
    key = value[1]

    print(self.locator)
    element = self.getElement(obj.driver, self.locator)
    select = Select(element)

    if (by == 'index'):
      if not isinstance(key, int): raise Exception('arg2 expects int type but received ' + str(key))
      select.select_by_index(key)
    elif (by == 'value'):
      select.select_by_value(str(key))
    elif (by == 'text'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + str(key))
      select.select_by_visible_text(str(key))
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

class FormRadios(ElementBase):
  def __init__(self, name: str):
    self.locateBy = By.XPATH
    self.xpathButton = '//input[@type="radio"][@name="%s"]' % name

  def __get__(self, obj, owner):
    locator = (self.locateBy, self.xpathButton)
    elements = obj.driver.find_elements(*locator)
    for element in elements:
      if element.is_selected():
        elemSelected = element
        break
    return elemSelected.get_attribute("value")

  def __set__(self, obj, value: tuple):
    setBy = str(value[0])
    key = str(value[1])

    # radio[@name={radio.name}] 自身
    xpathButton = self.xpathButton

    # ラベルがあればラジオボタンをラップするlabelをクリック対象に、なければラジオボタン自体をクリック対象にする
    if (setBy == 'index'):
      xpathWrapper = 'label[%s]' % xpathButton
      # labelsはあるか無いかわからないのでリストとして取得する
      labels = obj.driver.find_elements(self.locateBy, xpathWrapper)
      if labels[key]:
        target = labels[key]
      else:
        buttons = obj.driver.find_elements(self.locateBy, xpathButton)
        target = buttons[key]
    elif (setBy == 'value'):
      xpathButton = '%s[@value="%s"]' % (xpathButton, key)
      xpathWrapper = 'label[%s]' % xpathButton
      labels = obj.driver.find_elements(self.locateBy, xpathWrapper)
      if labels[0]:
        target = label
      else:
        target = self.getElement(obj.driver, xpathButton)
    target.click()


class FormCheckbox(ElementBase):
  def __init__(self, name: str):
    self.locator = (By.XPATH, '//*[@type="checkbox"][@name="' + name + '"]')

  def __get__(self, obj, owner):
    return self.getElement(obj.driver, self.locator)

  def __set__(self, obj, value: tuple):
    by = str(value[0])
    key = str(value[1])
    action = str(value[2])

    if (by == 'index'):
      xpath = self.locator[1] + '[' + key + ']'
      locator = (self.locator[0], xpath)
      element = self.getElement(obj.driver, locator)
    elif (by == 'value'):
      xpath = self.locator[1] + '[@value="' + key + '"]'
      locator = (self.locator[0], xpath)
      element = self.getElement(obj.driver, locator)
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

    state = element.is_selected()

    if (action == 'toggle'):
      element.click()
    elif (action == 'check'):
      if not state: element.click()
    elif (action == 'uncheck'):
      if state: element.click()
    else:
      raise Exception('invalid action ' + action  + ' for ' + __class__.__name__)