from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from .xpath import *

"""visit https://selenium-python.readthedocs.io/page-objects.html for more info"""

WAIT = 5
BY = 'xpath'

class ElementBase:
  def __init__(self, xpath: str):
    self.xpath = xpath

  def __get__(self, obj, owner):
    xpath = self.xpath
    return self.getElement(obj.driver, xpath).click()

  def __set__(self, obj, value):
    pass

  def getElement(self, driver, xpath) -> object :
    WebDriverWait(driver, WAIT).until(
      lambda driver: driver.find_element(BY, xpath))
    return driver.find_element(BY, xpath)

  def countElement(self, driver, xpath) -> int :
    return len(driver.find_elements(BY, xpath))

class LinkText(ElementBase):
  def __init__(self, text: str):
    base = LINK_TEXT
    option = '[.="%s"]' % (text)
    self.xpath = '//%s%s' % (base, option)


class LinkImage(ElementBase):
  def __init__(self, src: str):
    base = LINK_IMAGE
    option = '[img[@src="%s"]]' % (src)
    self.xpath = '//%s%s' % (base, option)

class FormText(ElementBase):
  def __init__(self, name: str):
    base = TEXT_INPUT
    option = '[@name="%s"]' % (name)
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    xpath = self.xpath
    element = self.getElement(obj.driver, xpath)
    return element.get_attribute("value")

  def __set__(self, obj, value):
    xpath = self.xpath
    element = self.getElement(obj.driver, xpath)
    element.clear()
    element.send_keys(value)

class FormSelect(ElementBase):
  def __init__(self, name: str):
    base = SELECT
    option = '[@name="%s"]' % (name)
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    xpath = self.xpath
    element = self.getElement(obj.driver, xpath)
    select = Select(element)
    return element.get_attribute("value")

  def __set__(self, obj, value: tuple):
    method = value[0]
    key = value[1]

    xpath = self.xpath
    element = self.getElement(obj.driver, xpath)
    element.click()
    select = Select(element)

    if (method == 'index'):
      if not isinstance(key, int): raise Exception('arg2 expects int type but received ' + str(key))
      xpathOption = '%s/option[%d]' % (xpath, key)
      WebDriverWait(obj.driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpath))
      select.select_by_index(key)
    elif (method == 'value'):
      xpathOption = '%s/option[@value="%s"]' % (xpath, key)
      WebDriverWait(obj.driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpath))
      select.select_by_value(str(key))
    elif (method == 'text'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + str(key))
      xpathOption = '%s/option[text()="%s"]' % (xpath, key)
      WebDriverWait(obj.driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpath))
      select.select_by_visible_text(str(key))
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

class FormRadios(ElementBase):
  def __init__(self, name: str):
    base = INPUT_RADIOS
    option = '[@name="%s"]' % (name)
    self.nodeInput = base + option
    self.xpath = '//' + base + option

  def __get__(self, obj, owner):
    elements = obj.driver.find_elements(BY, self.xpath)
    for element in elements:
      if element.is_selected():
        elemSelected = element
        break
    return elemSelected.get_attribute("value")

  def __set__(self, obj, value: tuple):
    method = value[0]
    key = value[1]

    nodeInput = self.nodeInput
    # 指定したnameを持つinputを囲むラベルがあればラベルをクリック対象に、なければinputを対象にする
    countWrapper = self.countElement(obj.driver, '//' + self.getWrapperNode(nodeInput))
    countFor = self.countElement(obj.driver, '//' + self.getForNode(nodeInput))

    if (method == 'index'):
      if ( countWrapper > 0 ):
        node = self.getWrapperNode(nodeInput)
      elif ( countFor > 0 ):
        node = self.getForNode(nodeInput)
      else:
        node = nodeInput
      xpath = '//' + node
      elements = obj.driver.find_elements(BY, xpath)
      element = elements[key]
    elif (method == 'value'):
      optionForButton = '[@value="%s"]' % (key)
      nodeInput += optionForButton
      node = self.getWrapperNode(nodeInput) if ( countWrapper > 0 ) else nodeInput
      xpath = '//' + node
      element = self.getElement(obj.driver, xpath)
    element.click()

  def getWrapperNode(self, nodeInput):
      return 'label' + WRAPS_INPUT % nodeInput

  def getForNode(self, nodeInput):
      return 'label' + WITH_INPUT % nodeInput
class FormCheckbox(ElementBase):
  def __init__(self, name: str):
    base = INPUT_CHECKBOXES
    option = '[@name="%s"]' % (name)
    self.nodeInput = base + option
    self.xpath = '//' + base + option

  def __get__(self, obj, owner):
    xpath = self.xpath
    return self.getElement(obj.driver, xpath)

  def __set__(self, obj, value: tuple):
    method = value[0]
    key = value[1]
    action = value[2]

    nodeInput = self.nodeInput
    # 指定したnameを持つinputを囲むラベルがあればラベルをクリック対象に、なければinputを対象にする
    countWrapper = self.countElement(obj.driver, '//' + self.getWrapperNode(nodeInput))

    if (method == 'index'):
      node = self.getWrapperNode(nodeInput) if ( countWrapper > 0 ) else nodeInput
      xpath = '//' + node
      elements = obj.driver.find_elements(BY, xpath)
      element = elements[key]
    elif (method == 'value'):
      optionForButton = '[@value="%s"]' % (key)
      nodeInput += optionForButton
      node = self.getWrapperNode(nodeInput) if ( countWrapper > 0 ) else nodeInput
      xpath = '//' + node
      element = self.getElement(obj.driver, xpath)
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

  def getWrapperNode(self, nodeInput):
      return 'label[descendant::%s]' % nodeInput