#!/usr/local/bin/python3
from modules.driver import getChromeDriver, screenShot

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
import datetime
import os
import sys

# env setting
count_1 = 1

def testTokyu():
  user = 'Tokyu109'
  password = 'Cpap2020'
  url = 'https://%s:%s@tempsecure.sportsoasis.co.jp/netent/input_index.html?school_flg=1&shop_id=sh80' % (user, password)
  #url = 'https://qiita.com/mochio/items/dc9935ee607895420186'

  imageTitle = 'xxx'

  # launch browser
  driver = getChromeDriver()

  try:
    # open page
    driver.get(url)
    imageTitle = driver.title

    footer = driver.find_element_by_xpath('/html/body/footer')

    inputBirthYear = driver.find_element_by_name('birth_year')
    Select(inputBirthYear).select_by_value('2010')
    inputBirthYear = driver.find_element_by_name('birth_month')
    Select(inputBirthYear).select_by_value('10')
    inputBirthYear = driver.find_element_by_name('birth_day')
    Select(inputBirthYear).select_by_value('09')

    sleep(1)

    actions = ActionChains(driver)
    actions.move_to_element(footer)
    actions.perform()

    #inputSchool = driver.find_element_by_xpath('//*[@id="school"]/div/label[1]/p')
    inputSchool = driver.find_element_by_xpath('//*[@id="school"]/div/label[1]/input')
    inputSchool.click()

    screenShot(driver, imageTitle)

  except Exception as e:
    sys.exc_info()
  finally:
    # close
    driver.close()
    driver.quit()
testTokyu()