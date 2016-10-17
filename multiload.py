# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:07:46 2016

This script helps users create a new CKAN dataset and upload multiple resources to it.

@author: saintlyvi
"""

import ckanclasses

#1 new or existing dataset?
#2 if new, create dataset (ask for attributes)
#3 if existing, search for dataset and get attributes
#4 get organization_name of dataset
#5 select folder with resources to be uploaded
#6 get list of resources in folder
#7 get upload urls from path
#8 get names from list
#9 add description to each list item

dataset_status = input('Are you creating a new dataset?\n')

print('Here\'s a list of all available organisations:\n')
all_orgs = ckanclasses.show('all','organisation')
print(all_orgs)
while True:    
    check_org = int(input('Type the number corresponding to the organisation to which you are adding a dataset\n'))
    dataset_org = all_orgs[check_org]
    print(dataset_org)
    double_check = input('Is this correct?\n')
    if double_check.lower().strip() == 'no':
        continue
    else:
        break

if dataset_status.lower().strip() == 'yes':
    print('Let\'s add your dataset\n')
    new_dataset = ckanclasses.Dataset()
    new_dataset.owner_org = dataset_org    
    new_dataset.title = input('Enter dataset title: ')
    new_dataset.name = new_dataset.title.replace(' ', '-').lower()
    new_dataset.author = input('Enter author\'s name: ')
    new_dataset.author_email = input('Enter author\'s email: ')
    new_dataset.maintainer = input('Enter maintainer\'s name: ')
    new_dataset.maintainer_email = input('Enter maintainer\'s email: ')
    
    check_private = input('Is this a public dataset?')
    if check_private.lower().strip() == 'no':
        new_dataset.private == 'true'
        
    print('Under what license are you publishing the dataset? \nA) Creative Commons Attribution \nB) Creative Commons Share Alike \nC) Not open \n')
    check_license = input('Type A, B or C for license type')
    if check_license == 'A':
        new_dataset.license_id = 'cc-by'
    elif check_license == 'B':
        new_dataset.license_id = 'cc-by-sa'
    elif check_license == 'C':
        new_dataset.license_id = 'other-closed'
    else:
        new_dataset.license_id = 'notspecified'
    