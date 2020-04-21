from ...page import *
from modules.driver import screenShot, screenShotFull

from selenium.webdriver.common.by import By

SEARCH = (By.NAME, 'q')
SUBMIT = (By.NAME, 'btnK')

class MainPage:
  search = FormTextElement(SEARCH)
  sButton = FormSubmitElement(SUBMIT)

  def __init__(self, driver):
    self.driver = driver

  def test(self):
    url = 'https://google.com'
    self.driver.get(url)
    self.search = 'dog'
    self.sButton.submit()
    screenShotFull(self.driver, self.driver.title)