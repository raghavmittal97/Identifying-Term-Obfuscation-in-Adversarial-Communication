"""
created by: Mohit Sharma

"""

import requests
obj = print(requests.get('http://api.conceptnet.io/related/c/en/president?filter=/c/en/vote').json())

