import json
m = {'id': 2, 'name': 'hussain'}

print(m)
n = json.dumps(m)
o = json.loads(n)
print(o)