import re
import os
import json
with open('folders.txt') as fp:
  fols = fp.readlines()
with open('urls.json') as fp:
  data = json.load(fp)
for fol in fols:
  if fol.strip() == '':
    continue
  fles = sorted(os.listdir(fol.strip()))
  names = [ { 'name': ((re.search(r'-[^-.]*', fle).group(0))[2:]).replace('_', ' ') } for fle in fles ]
  data.extend(names)
with open('urls.json', 'w') as fp:
  json.dump(data, fp, sort_keys=True, indent=2)
