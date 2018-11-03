import re
import os
import json
with open('queries.txt') as fp:
  queries = fp.readlines()
with open('urls.json') as fp:
  data = json.load(fp)
  names = [ { 'name': query.strip() } for query in queries if query.strip() != '']
  data.extend(names)
with open('urls.json', 'w') as fp:
  json.dump(data, fp, sort_keys=True, indent=2)
