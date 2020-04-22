from ...page import *
from modules.driver import screenShot, screenShotFull

from selenium.webdriver.common.by import By

SEARCH = (By.NAME, 'q')
SUBMIT = (By.NAME, 'btnK')
SELECT = (By.NAME, 'blood')

class MainPage:
  search = FormTextElement(SEARCH)
  sButton = FormSubmitElement(SUBMIT)

  bloodSelect = FormSelectElement(SELECT)

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    """
    url = 'https://google.com'
    self.search = 'dog'
    self.sButton.submit()
    """
    url = 'http://www.htmq.com/html/select.shtml'
    self.driver.get(url)
    self.bloodSelect = ('text', 'AB型')
    screenShotFull(self.driver, self.driver.title)