from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

"""visit https://selenium-python.readthedocs.io/page-objects.html for more info"""

WD = 100

class ElementBase:
  def __init__(self, locator: tuple):
    self.locator = locator
  def getElement(self, obj):
    driver = obj.driver
    WebDriverWait(driver, self.waitDuration).until(
        lambda driver: driver.find_element(*self.locator))
    return driver.find_element(*self.locator)

class FormTextElement(ElementBase):
  waitDuration = WD
  def __set__(self, obj, value):
    element = self.getElement(obj)
    element.clear()
    element.send_keys(value)
  def __get__(self, obj, owner):
    element = self.getElement(obj)
    return element.get_attribute("value")

class FormSubmitElement(ElementBase):
  waitDuration = WD
  def __get__(self, obj, owner):
    return self.getElement(obj)