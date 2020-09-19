from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

from .xpath import Xpath

"""visit https://selenium-python.readthedocs.io/page-objects.html for more info"""

WAIT = 5
BY = 'xpath'

class PageBase:
  def __init__(self, driver: webdriver):
    self.driver = driver

class ElementBase:
  def __init__(self, xpath: str):
    self.xpath = xpath

  def __get__(self, obj, owner):
    driver = obj.driver
    xpath = self.xpath
    return self.getElement(driver, xpath).click()

  def __set__(self, obj, value):
    pass

  def getElement(self, driver, xpath) -> object :
    WebDriverWait(driver, WAIT).until(
      lambda driver: driver.find_element(BY, xpath))
    return driver.find_element(BY, xpath)

  def countElement(self, driver, xpath) -> int :
    return len(driver.find_elements(BY, xpath))

  def getWrapperNode(self, nodeInput):
      return 'label' + Xpath.getOptionByWrappedInput(nodeInput)

  def getForNode(self, nodeInput):
      return 'label' + Xpath.getOptionByPairInput(nodeInput)

  def getNodeToClick(self, nodeInput: str, countWrapper: int, countFor: int):
      if ( countWrapper > 0 ):
        node = self.getWrapperNode(nodeInput)
      elif ( countFor > 0 ):
        node = self.getForNode(nodeInput)
      else:
        node = nodeInput
      return node

class LinkText(ElementBase):
  def __init__(self, text: str):
    base = Xpath.textLink
    option = '[.="%s"]' % (text)
    self.xpath = '//%s%s' % (base, option)


class LinkImage(ElementBase):
  def __init__(self, src: str):
    base = Xpath.imageLink
    option = '[img[@src="%s"]]' % (src)
    self.xpath = '//%s%s' % (base, option)

class FormText(ElementBase):
  def __init__(self, name: str):
    base = Xpath.formText
    option = '[@name="%s"]' % (name)
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    driver = obj.driver
    xpath = self.xpath
    element = self.getElement(driver, xpath)
    return element.get_attribute("value")

  def __set__(self, obj, value):
    driver = obj.driver
    xpath = self.xpath
    element = self.getElement(driver, xpath)
    element.clear()
    element.send_keys(value)

class FormSelect(ElementBase):
  def __init__(self, name: str):
    base = Xpath.formSelect
    option = '[@name="%s"]' % (name)
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    driver = obj.driver
    xpath = self.xpath
    element = self.getElement(driver, xpath)
    select = Select(element)
    selectedOp = select.all_selected_options
    list = []
    for element in selectedOp:
      list.append(element.text)
    return list

  def __set__(self, obj, value: tuple):
    driver = obj.driver
    method = value[0]
    key = value[1]

    xpath = self.xpath
    element = self.getElement(driver, xpath)
    element.click()
    select = Select(element)

    if (method == 'index'):
      if not isinstance(key, int): raise Exception('arg2 expects int type but received ' + str(key))
      xpathOption = '%s/option[%d]' % (xpath, key + 1)
      WebDriverWait(driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpathOption))
      select.select_by_index(key)
    elif (method == 'value'):
      xpathOption = '%s/option[@value="%s"]' % (xpath, key)
      WebDriverWait(driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpathOption))
      select.select_by_value(str(key))
    elif (method == 'text'):
      if not isinstance(key, str): raise Exception('arg2 expects str type but received ' + str(key))
      xpathOption = '%s/option[text()="%s"]' % (xpath, key)
      WebDriverWait(driver, WAIT).until(
        lambda driver: driver.find_element(BY, xpathOption))
      select.select_by_visible_text(str(key))
    else:
      raise Exception('arg1 expects "index", "value", or "text"')

class FormRadio(ElementBase):
  def __init__(self, name: str):
    base = Xpath.formRadio
    option = '[@name="%s"]' % (name)
    self.nodeInput = base + option
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    driver = obj.driver
    elements = driver.find_elements(BY, self.xpath)
    for element in elements:
      if element.is_selected():
        elemSelected = element
        break
    return elemSelected.get_attribute("value")

  def __set__(self, obj, value: tuple):
    driver = obj.driver
    method = value[0]
    key = value[1]

    nodeInput = self.nodeInput
    # 指定したnameを持つinputに対応するラベルをクリック対象に、なければinputを対象にする
    nodeLabel = Xpath.getLabelbyInput(nodeInput)
    countLabel = self.countElement(driver, '//' + nodeLabel)

    if (method == 'index'):
      node = Xpath.getLabelbyInput(nodeInput) if ( countLabel > 0 ) else nodeInput
      xpath = '//%s' % (node)
      WebDriverWait(driver, WAIT).until(
        lambda driver: len(driver.find_elements(BY, xpath)) >= key + 1 )
      elements = driver.find_elements(BY, xpath)
      element = elements[key]
    elif (method == 'value'):
      optionForInput = '[@value="%s"]' % (key)
      nodeInput += optionForInput
      node = Xpath.getLabelbyInput(nodeInput) if ( countLabel > 0 ) else nodeInput
      xpath = '//%s' % (node)
      element = self.getElement(driver, xpath)
    elif (method == 'label'):
      optionForLabel = '[.="%s"]' % (key)
      node = Xpath.getLabelbyInput(nodeInput) + optionForLabel
      xpath = '//%s' % (node)
      element = self.getElement(driver, xpath)
    else:
      raise Exception('arg1 expects "index", "value", or "text"')
    element.click()

class FormCheckbox(ElementBase):
  def __init__(self, name: str):
    base = Xpath.formCheckbox
    option = '[@name="%s"]' % (name)
    self.nodeInput = base + option
    self.xpath = '//%s%s' % (base, option)

  def __get__(self, obj, owner):
    driver = obj.driver
    xpath = self.xpath
    return self.getElement(driver, xpath)

  def __set__(self, obj, value: tuple):
    driver = obj.driver
    method = value[0]
    key = value[1]
    action = value[2]

    nodeInput = self.nodeInput
    # 指定したnameを持つinputに対応するラベルをクリック対象に、なければinputを対象にする
    nodeLabel = Xpath.getLabelbyInput(nodeInput)
    countLabel = self.countElement(driver, '//' + nodeLabel)

    if (method == 'index'):
      node = Xpath.getLabelbyInput(nodeInput) if ( countLabel > 0 ) else nodeInput
      xpath = '//%s' % (node)
      WebDriverWait(driver, WAIT).until(
        lambda driver: len(driver.find_elements(BY, xpath)) >= key + 1 )
      elements = driver.find_elements(BY, xpath)
      element = elements[key]
    elif (method == 'value'):
      optionForInput = '[@value="%s"]' % (key)
      nodeInput += optionForInput
      node = Xpath.getLabelbyInput(nodeInput) if ( countLabel > 0 ) else nodeInput
      xpath = '//%s' % (node)
      element = self.getElement(driver, xpath)
    elif (method == 'label'):
      optionForLabel = '[.="%s"]' % (key)
      node = Xpath.getLabelbyInput(nodeInput)
      xpath = '//%s' % (node)
      element = self.getElement(driver, xpath)
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
      raise Exception('arg2 expects "toggle", "check", or "uncheck"')