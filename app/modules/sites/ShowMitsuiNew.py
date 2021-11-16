import requests
from bs4 import BeautifulSoup

def ShowMitsuiNew():
  url = 'https://mfr.rehouse.co.jp'
  r = requests.get(url)
  soup = BeautifulSoup(r.text)

  ## title and description
  title = soup.title.text
  d = soup.find(attrs={'name': 'description'})
  description = d['content']
  k = soup.find(attrs={'name': 'keywords'})
  description = d['content']

  ns = soup.find('noscript').extract()

  ex = soup.find_all(attrs={'href': True})
  for e in ex:
      href = e['href']
      if href.startswith('/'):
        e['href'] = url + href
  sr = soup.find_all(attrs={'src': True})
  for s in sr:
      src = s['src']
      if src.startswith('/'):
        s['src'] = url + src

  contents = soup.main.find_all()
  for c in contents:
    c.extract()
  ex = soup.main.find_all()

  with open("tmp/NewLayout.html", "w") as text_file:
    text_file.write(str(soup))
  return str(title)