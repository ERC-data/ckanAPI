# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 14:56:57 2016

Simple examples using the official ckanapi Python module

@author: saintlyvi
"""
    
import os 
from ckanapi import RemoteCKAN, NotAuthorized # submodule to use for accessing a remote ckan instance from laptop

# Set your API key
apikey = '' 

# Set your CKAN remote destination
site = RemoteCKAN('http://energydata.uct.ac.za', apikey)

###########################
# A typical GET command
###########################
erc_datalib = site.action.organization_show(id='erc-datalibrary', include_datasets='True', include_users='False') #returns a dict

# Analysing your retrieved dictionary resource
d = erc_datalib

keys = d.keys()

for k in keys: 
    if isinstance(d[k], (str, int)): # check if dict value is a string or integer and print value if True
        print(k, ":", d[k])
    elif isinstance(d[k], (list)): # check if dict value is a list
        if len(d[k]) > 0:
            print(len(d[k]), k) # if non-empty list print length of list
        else:
            print(k, ": empty list")
    else:
        print(k, type(d[k]))

for k in keys: 
    if isinstance(d[k], (list)): # check if dict value is a list
        if len(d[k]) > 0:
            for i in list(range(0, len(d[k]))):
                if isinstance(d[k][i], (dict)): 
                    if i == 0:
                        print(k, ":", d[k][0].keys()) # if non-empty list print keys of first list item
                        print(k, 'names :')
                        print("* ", d[k][i].get('name')) # 
                    else:
                        print("* ", d[k][i].get('name'))
                else:
                    print("data type of list item %d is a" % (i), type(d[k][i]))
                    
# Analysing your retrieved list resource
    
###########################
# A typical POST command
###########################
# Create a new dataset
try:
    pkg = site.action.package_create(name='waterberg-air-quality', title='Waterberg Air Quality Data', author='Thabo Setshedi', author_email= 'TSetshedi@environment.gov.za', maintainer='Katye Alterie', maintainer_email='kalterie@uct.ac.za', license_id='cc-by', private='true', owner_org='erc-datalibrary', notes='This dataset contains data from the Department of Environmental Affairs for the following stations in the Waterberg:\r\n\r\n  *  Lephalale\r\n  *  Mokopane\r\n  *  Thabazimbi', extras= [{'key':'Data location', 'value':'server'}, {'key':'FTP capability', 'value':'yes'},{'key':'Raw files', 'value':'yes'}])
except NotAuthorized:
    print('denied')
    
try:
    pkg = site.action.package_create(name='mpumalanga-eskom-air-quality', title='Mpumalanga Air Quality Data from Eskom', author='Gerhardt de Beer', author_email= 'DBeerGH@eskom.co.za', maintainer='Samantha Keen', maintainer_email='samantha.keen@uct.ac.za', license_id='other-closed', private='true', owner_org='erc-datalibrary', notes='This dataset contains data from Eskom for the following stations in Mpumalanga:\r\n\r\n  *  Camden\r\n  *  Grootvlei\r\n  *  Grootdraaidam\r\n  *  Elandsfontein\r\n  *  Komati\r\n  *  Leandra\r\n  *  Majuba\r\n  *  Phola\r\n  *  Verkykkop', extras= [{'key':'Data location', 'value':'SAAQIS'}, {'key':'FTP capability', 'value':'not configured'},{'key':'DMS', 'value':'Enviroload software'},{'key':'Raw files', 'value':'no'}])
except NotAuthorized:
    print('denied')
    
    
# Add a resource to the dataset
site.action.resource_create(package_id='waterberg-air-quality', upload=open('/home/saintlyvi/Documents/ckan data library/Limpopo_AQD/Waterberg/Lephalale1.csv', 'rb'), url='', name='Lephalale 2012', description='Parameters monitored:\r\n \r\n\r\nStart Date of reporting to SAAQIS:\r\n \r\n\r\nLast Date reporting to SAAQIS:\r\n')    
    
# Make the dataset private
try:
    site.action.update_package(id='waterberg-air-quality', private='true') 
except NotAuthorized:
    print('denied')    
    
##################################
# Adding datasets and resources    
##################################
    
path = os.getcwd() # get current working directory ... you can also set path explicitly
files = os.listdir(path) # create list of all files at path
for idx, f in enumerate(files): # append full path name to file name
    files[idx] = path + f   
    
