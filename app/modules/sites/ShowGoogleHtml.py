import requests
from bs4 import BeautifulSoup
from modules.XpathBuilder import XpathBuilder
from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen

def ShowGoogleHtml():
  # selector
  x = XpathBuilder()
  x.set('input[@type=text]')
  #url = 'https://google.com'
  url = 'https://www.rehouse.co.jp'
  r = requests.get(url)
  soup = BeautifulSoup(r.text)

  ## title and description
  title = soup.title.text
  d = soup.find(attrs={'name': 'description'})
  description = d['content']
  k = soup.find(attrs={'name': 'keywords'})
  description = d['content']

  target = soup.find('body')
  target.header.extract()
  target.footer.extract()
  target.name = 'div'

  head = soup.find('head')
  sc = head.find_all('script', href=True)
  test = [c['href'] for c in sc]
  css = head.find_all('link', rel='stylesheet')
  test = [c['href'] for c in css]
  mt = head.find_all('meta')
  test = [m.get('content', None) for m in mt]

  with open("tmp/Output.html", "w") as text_file:
      text_file.write(str(target))
  with open("tmp/Head.html", "w") as text_file:
      text_file.write(str(head))
  with open("tmp/Original.html", "w") as text_file:
      text_file.write(str(soup))
  return str(test)
  return str(description)
  """
  driver = getChromeDriver()
  driver.get(url)
  """
  return x.build()