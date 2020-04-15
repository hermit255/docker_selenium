#!/usr/local/bin/python3
from selenium import webdriver

def collectInputs(driver: webdriver, option: str = None):
  tags = []
  elements = driver.find_elements_by_tag_name('input')
  for element in elements:
    if not option:
      tag = {}
      tag['location'] = element.location
      tag['type'] = element.get_attribute('type')
      tag['name'] = element.get_attribute('name')
      tag['value'] = element.get_attribute('value')
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