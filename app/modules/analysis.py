#!/usr/local/bin/python3
from selenium import webdriver

def collectInputs(driver: webdriver, option: str = None):
  tags = []
  elements = driver.find_elements_by_tag_name('input')
  for element in elements:
    if not option:
      tag = {}
      tag['name'] = element.get_attribute('name')
      tag['value'] = element.get_attribute('value')
      location = element.location
      tag['location_x'] = location['x']
      tag['location_y'] = location['y']
      tag['type'] = element.get_attribute('type')
      if tag['type'] != 'hidden' and tag['type'] != 'submit':
        tag['title'] = getTitle(element)
      else:
        tag['title'] = tag['value']
      tags.append(tag)
  return tags

def exceptHiddenInput(tag: list):
  return tag['type'] != 'hidden'

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

def getTitle(element):
  try:
    while element.text == '':
      element = element.find_element_by_xpath('..')
    return element.text
  except Exception as e:
    print(e)
    return 'noLabel'