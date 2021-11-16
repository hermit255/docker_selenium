import requests
import re
from bs4 import BeautifulSoup
from modules.XpathBuilder import XpathBuilder
from modules.driver import getChromeDriver, getChromeHeadlessDriver, screenShot, fullScreen

def ShowMitsuiOld():
  host = 'https://www.rehouse.co.jp'
  urls = [
      {'name': 'top', 'url': host},
      {'name': 'buyerTop', 'url': host + '/buyers/fund/index.html'},
      {'name': 'carShare', 'url': host + '/carshare/index.html'},
      {'name': 'carShareMerit', 'url': host + '/carshare/merit/index.html'},
      {'name': 'carShareSim', 'url': host + '/carshare/simulation/index.html'},
      {'name': 'consult', 'url': host + '/consultation/index.html'},
  ]
  for v in urls:
      genFile(v['url'], v['name'], host)
  return 'complete!'

def genFile(url: str, name: str, host: str):
  r = requests.get(url)
  soup = BeautifulSoup(r.content)

  ## title and description
  #title = soup.title.text
  #d = soup.find(attrs={'name': 'description'})
  #description = d['content']
  #k = soup.find(attrs={'name': 'keywords'})
  #description = d['content']

  ns = soup.find('noscript')
  if ns:
      ns.extract()

  ex = soup.find_all(attrs={'href': True})
  for v in ex:
      href = v['href'].replace('//www.rehouse.co.jp', '')
      if href.startswith('/'):
        v['href'] = host + href
  sr = soup.find_all(attrs={'src': True})
  for v in sr:
      src = v['src'].replace('//www.rehouse.co.jp', '')
      if src.startswith('/'):
        v['src'] = host + src

  attrName = 'data-src'
  ds = soup.find_all(attrs={attrName: True})
  for v in ds:
      attr = v[attrName].replace('//www.rehouse.co.jp', '')
      if attr.startswith('/'):
        attr = host + attr
      if v.name == 'img':
        newAttr = 'src'
        v[newAttr] = attr
      if v.name != 'img':
        newAttr = 'style'
        v[newAttr] = f'background-image: url("{attr}")'

  attrName = 'style'
  withSt = soup.find_all(attrs={attrName: True})
  for v in withSt:
      v[attrName].replace('background-image: url("/', 'background-image: url("' + host)

  target = soup.find('body')
  target.header.extract()
  target.footer.extract()
  target.name = 'div'
  sc = target.find_all('script')
  for v in sc:
      target.append(v)

  head = soup.find('head')
  if head:
    sc = head.find_all('script', href=True)
    css = head.find_all('link', rel='stylesheet')
    style = head.find_all('style')

    for v in css:
      target.append(v)
    for v in style:
      target.append(v)
    mt = head.find_all('meta')

  #with open("tmp/OldBody.html", "w") as text_file:
  #    text_file.write(str(target))
  #with open("tmp/Head.html", "w") as text_file:
  #    text_file.write(str(head))
  #with open("tmp/OldOriginal.html", "w") as text_file:
  #    text_file.write(str(soup))

  with open("tmp/NewLayout.html", "r") as x:
      new = BeautifulSoup(x)
      new.find('main').append(target)
  with open(f'tmp/{name}.html', "w") as x:
      x.write(str(new))