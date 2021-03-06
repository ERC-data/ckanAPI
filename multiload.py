# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:07:46 2016

This script helps users create a new CKAN dataset and upload multiple resources to it.

@author: saintlyvi
"""

import ckanclasses, ckanfunctions
import pandas as pd
import numpy as np

# Section 1: Dataset creation or selection
print('********************\nThis section helps you create or select a dataset to update.\n********************\n')
dataset_status = input('Are you creating a new dataset?\n')

if dataset_status.lower().strip() != 'no':
    dataset = ckanfunctions.new_dataset()    
else:    
    dataset = ckanfunctions.search_dataset()

# Section 2: Adding resources for upload to dataset
print('\n********************\nThis section helps you upload multiple resources to your dataset.\n********************')

# get list of resources in folder
(resource_folder, resource_list) = ckanfunctions.select_folder()

#resource_names = [r[:-4] for r in resource_list]

while True:    
    # get upload urls from path
    resource_upload = ckanfunctions.upload_files(resource_list)
    
    upload_paths = []
    resource_names = []
    for r in resource_upload:
        r_path = '/'.join([resource_folder, resource_list[r]])
        upload_paths.append(r_path)
        resource_names.append(resource_list[r].split('.', 1)[0])
        
    # create dataframe containing all resource upload data
    resources = pd.DataFrame({'package_id':dataset.name , 'name':resource_names, 'upload':upload_paths, 'description':'', 'url':'unused-but-required', 'id':np.nan})
    
    # add description to each list item
    all_resources = ckanfunctions.resource_descriptions(resources)
    
    final_check = input('Are you ready to commence your multiresource-upload? Press enter to continue or type \'no\' to make changes.\n')
    if final_check.lower().strip() != 'no':
        break
    else:
        while True:        
            check_file = int(input('Which file do you want to change (type number)?\n') or 0)
            print(all_resources['name'][check_file])
            print('ATTRIBUTES: ', list(all_resources.columns))
            make_change = input('Type the attribute you want to change\n').lower().strip()
            new_attr = input('Enter %s\n' % make_change)
            all_resources.loc[check_file, make_change] = new_attr
            print(all_resources.ix[check_file])
            double_check = input('Is this correct?\n')
            if double_check.lower().strip() == 'no':
                continue
            else:
                more_change = input('Do you want to change any other files?\n')
                if more_change.lower().strip() == 'no':
                    break
                else:
                    continue
            break
    break
                
# Section 3: Uploading resources to dataset
print('\n********************\nYour resources are being uploaded. Please be patient and confirm their availability online.\n********************')

for i in all_resources.index:
    my_resource = ckanclasses.Resource(package_id=all_resources['package_id'][i], name=all_resources['name'][i], description=all_resources['description'][i], url=all_resources['url'][i], upload=all_resources['upload'][i])
    try:
        my_resource.create()
        my_resource.create_view()
        all_resources.loc[i, 'id'] = my_resource.id
    except:
        print('Failed to upload %s' % all_resources['name'][i])
        