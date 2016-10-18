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
dataset = ckanclasses.Dataset()

#User input to create parameters for new dataset
if dataset_status.lower().strip() != 'no':

    print('Here\'s a list of all available organisations:\n')
    all_orgs = ckanclasses.show('all','organisation')
    print(all_orgs)
    while True:    
        check_org = int(input('Type the number corresponding to the organisation to which you are adding a dataset\n') or 2)
        dataset_org = all_orgs[check_org]
        print(dataset_org)
        double_check = input('Is this correct?\n')
        if double_check.lower().strip() == 'no':
            continue
        else:
            break

    print('Let\'s add your dataset')
    dataset.owner_org = dataset_org    
    dataset.title = input('Enter dataset title: ')
    dataset.name = dataset.title.replace(' ', '-').lower()
    dataset.author = input('Enter author\'s name: ')
    dataset.author_email = input('Enter author\'s email: ')
    dataset.maintainer = input('Enter maintainer\'s name: ')
    dataset.maintainer_email = input('Enter maintainer\'s email: ')
    
    check_private = input('Is this a public dataset? ')
    if check_private.lower().strip() == 'no':
        dataset.private = 'true'
    else:
        dataset.private = 'false'
        
    print('\nUnder what license are you publishing the dataset? \nA) Creative Commons Attribution \nB) Creative Commons Share Alike \nC) Not open \n')
    check_license = input('Type A, B or C for license type\n')
    if check_license == 'A':
        dataset.license_id = 'cc-by'
    elif check_license == 'B':
        dataset.license_id = 'cc-by-sa'
    elif check_license == 'C':
        dataset.license_id = 'other-closed'
    else:
        dataset.license_id = 'notspecified'
    
    print('\nYou have specified the following details for the dataset to be created\n')
    while True:
        print(dataset.check())
        double_check = input('Is this correct?\n')
        if double_check.lower().strip() == 'no':
            print('\nWhich attribute do you want to change?')
            print(dataset.attributes)
            make_change = input('Type the selected attribute\n').lower().strip()
            new_attr = input('Enter %s\n' % make_change)
            setattr(dataset, make_change, new_attr)
            continue
        else:
            break
            
else:    
    while True:
        search = input('Type a search term for the dataset you want to update\n')
        s = ckanclasses.search(search, 'dataset')
        print(s)
        if s.shape[1] == 1:
            check_dataset = input('Is this the dataset you are looking for?\n')
            if check_dataset.lower().strip() != 'no':
                dataset.name = s.ix['name'][0]
                break
            else:
                continue
        else:
            try:
                search_dataset = int(input('Type the number corresponding to your dataset (or press enter if None)\n'))
            except ValueError:
                check_private = input('Is this a public dataset? ')
                if check_private.lower().strip() == 'no':
                    dataset.name = input('Please enter the dataset name - this is the lower-case-hyphenated-word-string at the end of the online url\n')
                    if dataset.name == '':
                        print('You have not specified a dataset to update')
                        continue
                    else:
                        break
                else:
                    continue
            
            while True:
                print(s.ix[[search_dataset]])
                check_dataset = input('Is this the dataset you are looking for?\n')
                if check_dataset.lower().strip() != 'no':
                    dataset.name = s['name'][search_dataset]
                    break
                else:
                    search_dataset = int(input('Type the number corresponding to your dataset\n'))
                    continue
            break

           
                