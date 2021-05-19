import json

data = {'best credit cards':'best credit cards', 'best covid loans':'best covid loans', 'best renovation loans':'best renovation loans'}

with open('keyword_list.json', 'w') as outfile:
    json.dump(data, outfile)