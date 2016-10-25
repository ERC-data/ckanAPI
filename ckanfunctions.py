# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:13:45 2016

This script contains functions that guide users through perfoming the following CKAN actions:
* create a new dataset
* search existing datasets
* select a number of resources to upload

@author: saintlyvi
"""

import ckanclasses
import os
import pandas as pd

def new_dataset():
    """Prompt user input to create parameters for new dataset"""
    dataset = ckanclasses.Dataset()
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
    check_license = input('Type A, B or C for license type\n').lower().strip()
    if check_license == 'a':
        dataset.license_id = 'cc-by'
    elif check_license == 'b':
        dataset.license_id = 'cc-by-sa'
    elif check_license == 'c':
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
            print('...creating dataset...\n')
            try:        
                dataset.create()
                break
            except ckanclasses.CKANAPIError:
                check_fail = input('Your dataset could not be created. Press enter to try again and check that all attributes are specified correctly or type \'quit\' to exit.\n')
                if check_fail.lower().strip() == 'quit':
                    break
                else:
                    continue
                
def search_dataset():
    """Prompt user input to search for an existing dataset"""
    dataset = ckanclasses.Dataset()
    while True:
        search = input('Type a search term for the dataset you want to update\n')
        s = ckanclasses.search(search, 'dataset')
        print(s)
        try:
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
                            return(dataset)
                    else:
                        continue
                
                while True:
                    print(s.ix[[search_dataset]])
                    check_dataset = input('Is this the dataset you are looking for?\n')
                    if check_dataset.lower().strip() != 'no':
                        dataset.name = s['name'][search_dataset]
                        return(dataset)
                    else:
                        search_dataset = int(input('Type the number corresponding to your dataset\n'))
                        continue
                
                return(dataset)
        
        except AttributeError:
                continue

def select_folder():
    """Prompt user input to select a folder containing resources"""
    while True:
        try:
            resource_folder = input('Enter the PATH to the folder containing the resources you want to add\n')
            resource_list = os.listdir(resource_folder)
            print(pd.Series(resource_list))
            folder_check = input('Is this the right folder?\n')
            if folder_check.lower().strip() == 'no':
                continue
            else:
                return(resource_folder, resource_list)
        except FileNotFoundError:
            check_quit = input('The PATH does not exist. Press enter to try again or type \'quit\' to exit.\n')
            if check_quit.lower().strip() == 'quit':
                return()
            else:
                continue
            
def upload_files(resource_list):
    upload_select = "".join(input('List the number corresponding to the resources to be included (indicate range with \'-\' , comma separate list of numbers and type \'all\' or press enter to select all resources)\n').split())
    resource_upload = []
    if '-' in upload_select: 
        num_start = int(upload_select.split("-", 1)[0])
        num_end = int(upload_select.split("-", 1)[1])
        resource_upload = list(range(num_start, num_end + 1))
    elif ',' in upload_select:
        resource_upload = list(map(int, upload_select.split(','))) # split input list by commas, map strings to integers, convert to list
    elif upload_select == 'all' or upload_select == '':
        resource_upload = list(range(0, len(resource_list)))
    else:
        upload_single = int(upload_select)
        resource_upload = resource_upload.append(upload_single)
    return(resource_upload)
    
def resource_descriptions(resources):
    description_check = input('Would you like to add a description to each resource?\n')        
    if description_check.lower().strip() == 'no':
        pass
    else:
        descriptions = []
        for r in resources.index:
            d = input('Enter dataset description for %s\n' % resources['name'][r])
            descriptions.append(d)
        resources['description'] = descriptions
    print('These are your files to upload\n\n', resources)
    return(resources)