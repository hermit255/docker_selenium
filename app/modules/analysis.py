#!/usr/local/bin/python3
from modules.conf import dirCsv

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup

import csv

def getAsJson(element: WebElement):
  html = element.get_attribute('outerHTML')
  return bs4(html, 'html.parser').a.attrs

def getFormItems(driver: webdriver):
  tags = []

  inputs = driver.find_elements_by_tag_name('input')
  for element in inputs:
    tag = {}
    tag['label'] = getLabel(element)
    tag['id'] = element.get_attribute('id')
    tag['name'] = element.get_attribute('name')
    tag['type'] = element.get_attribute('type')
    tag['value'] = element.get_attribute('value')
    location = element.location
    tag['location_x'] = location['x']
    tag['location_y'] = location['y']
    tags.append(tag)

  selects = driver.find_elements_by_tag_name('select')
  for element in selects:
    tag = {}
    tag['label'] = getLabel(element)
    tag['id'] = element.get_attribute('id')
    tag['name'] = element.get_attribute('name')
    tag['type'] = 'select'
    tag['value'] = getSelectOptions(element)
    location = element.location
    tag['location_x'] = location['x']
    tag['location_y'] = location['y']
    tags.append(tag)
  return tags

def collectLinks(driver: webdriver):
  tags = []
  elements = driver.find_elements_by_tag_name('a')
  for element in elements:
    tag = {}
    tag['location'] = element.location
    tag['text'] = element.text
    tag['href'] = element.get_attribute('href')
    tags.append(tag)
  return tags

def getLabel(element):
  try:
    id = element.get_attribute('id')
    if id:
      labels = element.find_elements_by_xpath('../label[@for="{}"]'.format(id))
      if labels:
        return labels[0].get_attribute('textContent')
      else:
        while not element.get_attribute('textContent'):
          element = element.find_element_by_xpath('..')
        return '(maybe)' + element.get_attribute('textContent')
    else:
      return ''
  except Exception as e:
    print(e)
    return 'error'

def getSelectOptions(element):
  select = Select(element)
  selected = select.all_selected_options
  options = select.options
  tags = []
  for option in options:
    tag = {}
    tag['value'] = option.get_attribute('value')
    tag['label'] = option.get_attribute('textContent')
    if option in selected: tag['selected'] = 1
    tags.append(tag)
  return tags

def createCsv(tags: list, fullPath: str = None):
  defaultName = 'dName' + '.csv'
  fullPath = (dirCsv + defaultName) if fullPath is None else fullPath

  array = list(map(lambda tag: tag.values(), tags))
  with open(fullPath, 'w',  encoding='shift_jis') as f:
    writer = csv.writer(f)
    writer.writerow(tags[0])
    writer.writerows(array)