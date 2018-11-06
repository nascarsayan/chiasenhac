from urllib.parse import quote, urlencode
from collections import OrderedDict
import os
import json
from lxml import html, etree
from lxml.html.clean import clean_html
import requests
from time import sleep
import urllib.request as urllib2

CSN = 'http://search.chiasenhac.vn/search.php'

def main():
  data = []
  try:
    with open('urls.json') as fp:
      data = json.load(fp)
      l = len(data)
      for idx, edata in enumerate(data):
        if 'status' not in edata or edata['status'] == 'no':
          print('Downloading %3d of %3d : %s' % (idx + 1, l, edata['name']))
          mlink = ''
          if 'url' not in edata:
            qual = 1
            found = False
            while not found:
              response = requests.get(CSN, params={'s': edata['name']})
              # print(response.content)
              tree = html.fromstring((clean_html(response.content)).strip())
              page1 = tree.xpath("//table[@class='tbtable'][1]//tr[2]//td[2]//a[@class='musictitle']/@href")[0]
              response = requests.get(page1)
              # print(response.content)
              tree = html.fromstring((clean_html(response.content)).strip())
              page2 = tree.xpath("//img[@src='http://data.chiasenhac.com/images/button_download.gif']/../@href")[0]
              response = requests.get(page2)
              # print(response.content)
              tree = html.fromstring((clean_html(response.content)).strip())
              mlink = tree.xpath("//div[@id='downloadlink2']//a[last() - %d]/@href" %(qual))[0]
              request = urllib2.Request(mlink)
              request.get_method = lambda : 'HEAD'
              response = urllib2.urlopen(request)
              if 'http://chiasenhac.vn/' not in response.url:
                found = True
              else:
                print('Reducing quality')
                qual += 1
          else:
            mlink = edata['url']
          os.system('aria2c "%s" -d ./downloads' % (mlink))
          data[idx]['url'] = mlink
          data[idx]['status'] = 'yes'
          sleep(1)
        else:
          print('Already downloaded %3d of %3d : %s' % (idx + 1, l, edata['name']))
  except FileNotFoundError as fe:
    print('Creating urls.json... Rerun code')
  finally:
    if len(data) > 0:
      data[-1]['status'] = 'no'
    if os.path.isfile('urls.json'):
      with open('urls.json', 'r') as fp:
        data2 = json.load(fp)
        data = data + data2[len(data):]
    with open('urls.json', 'w') as fp:
      json.dump(data, fp, sort_keys=True, indent=2)

main()
