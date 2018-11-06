from urllib.parse import quote, urlencode
from collections import OrderedDict
import os
import json
from lxml import html, etree
from lxml.html.clean import clean_html
import requests
from time import sleep
import urllib.request as urllib2
from sys import argv

CSN = 'http://search.chiasenhac.vn/search.php'

def main():
  quan = int(argv[1])
  query = ' '.join(argv[2:])
  page = 1
  curr = 0
  while (curr < quan):
    response = requests.get(CSN, params={'s': query, 'page': page})
    # print(response.content)
    treem = html.fromstring((clean_html(response.content)).strip())
    cntpage = len(treem.xpath("//table[@class='tbtable'][1]//tr[@title]"))
    for idx in range(cntpage):
      if (curr == quan):
        break
      try:
        page1 = treem.xpath("//table[@class='tbtable'][1]//tr[@title][%d]/td[2]//a[@class='musictitle']/@href" % (idx + 1))[0]
        title = treem.xpath("//table[@class='tbtable'][1]//tr[@title][%d]/td[2]//a//text()" % (idx + 1))[0]
        print('Downloading %3d of %3d : %s' % (curr + 1, quan, title))
        response = requests.get(page1)
        tree = html.fromstring((clean_html(response.content)).strip())
        page2 = tree.xpath("//img[@src='http://data.chiasenhac.com/images/button_download.gif']/../@href")[0]
        response = requests.get(page2)
        qual = 1
        found = False
        tree2 = html.fromstring((clean_html(response.content)).strip())
        while not found:
          try:
            mlink = tree2.xpath("//div[@id='downloadlink2']//a[last() - %d]/@href" %(qual))[0]
            request = urllib2.Request(mlink)
            print(mlink)
            request.get_method = lambda : 'HEAD'
            response = urllib2.urlopen(request)
            if 'http://chiasenhac.vn/' not in response.url:
              found = True
            else:
              print('Reducing quality')
              qual += 1
          except Exception as e:
            print('Reducing quality')
            qual += 1
        os.system('aria2c "%s" -d ./downloads' % (mlink))
        sleep(1)
      except Exception as e:
        print(e)
      curr += 1
    page += 1
main()
