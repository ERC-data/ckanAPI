#!/home/saintlyvi/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
This script imports a dataset into CKAN

@author: saintlyvi
"""

import urllib.request, urllib.parse
import json
import pprint

######################
# Retrieving Data
######################

# Select desired CKAN API GET action function and specify data id (organization, package, resource, group, etc)
query= 'organization_show'
query_id='erc-datalibrary'

# Set the parts that make up your full url. If unsure of the inputs, the function can be reverse engineered with urllib.parse.urlparse(your_url)
scheme='http'
netloc='energydata.uct.ac.za'
path='/api/3/action/' + query.replace(" ", "")
params=''
query= urllib.parse.urlencode({'id': query_id})
fragment=''

# Make the HTTP request.
req=urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
response = urllib.request.urlopen(req)
assert response.code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.read().decode("utf-8"))

# Check the contents of the response.
assert response_dict["success"] is True
result = response_dict["result"]
pprint.pprint(result)

######################
# Posting Data
######################

# Select your desired CKAN API POST action function (create, update, patch, delete)
action= 'package_create'
api_key= '92bc3556-a1ef-44bb-b637-4df926e8bbea' # your API key

# Set the parts that make up your full url. If unsure of the inputs, the function can be reverse engineered with urllib.parse.urlparse(your_url)
scheme='http'
netloc='energydata.uct.ac.za'
path='/api/3/action/' + action.replace(" ", "")
params=''
query= ''
fragment=''
url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))

# Set data values to be posted 
values = {
    'name': 'waterberg-air-quality',
    'title': 'Waterberg Air Quality Data',
    'author': 'Thabo Setshedi',
    'author_email': 'TSetshedi@environment.gov.za',
    'maintainer': 'Katye Alterie',
    'maintainer_email': 'kalterie@uct.ac.za',
    'license_id': '',
    'notes': 'This dataset contains data from the Department of Environmental Affairs for the following stations in the Vaal Triangle: \Lephalale \Mokopane \Thabazimbi',
    'owner_org': 'erc-datalibrary',
    'extra': [{'key':'Data location', 'value':'server'}, {'key':'FTP capability', 'value':'yes'},{'key':'Raw files', 'value':'yes'}]
}

# Turn data dict into stringdata = urllib.parse.quote(json.dumps(values))

data = data.encode("utf-8") # data must be bytes when used with Request

req = urllib.request.Request(url, data) # Request is a POST if data parameter is specified
req.add_header('Authorization', api_key)

# Make the http request
response = urllib.request.urlopen(req)
assert response.code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.read())
assert response_dict['success'] is True

# package_create returns the created package as its result.
created_package = response_dict['result']
pprint.pprint(created_package)
