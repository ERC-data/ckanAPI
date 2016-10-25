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

while True:    
    # get upload urls from path
    resource_upload = ckanfunctions.upload_files(resource_list)
    
    upload_paths = []
    for r in resource_upload:
        r_path = '/'.join([resource_folder, resource_list[r]])
        upload_paths.append(r_path)
    
    # create dataframe containing all resource upload data
    resources = pd.DataFrame({'package_id':dataset.name , 'name':resource_list, 'upload':upload_paths, 'description':np.nan, 'url':'unused-but-required'})
    
    # add description to each list item
    all_resources = ckanfunctions.resource_descriptions(resources)
    
    final_check = input('Are you ready to commence your multiresource-upload? Press enter to continue or type \'no\' to make changes.')
    if final_check.lower().strip() != 'no':
        break
    else:
        print(pd.Series(resource_list))
        continue
    
# Section 3: Uploading resources to dataset
print('\n********************\nYour resources are being uploaded. Please be patient and confirm their availability online.\n********************')

for i in all_resources.index:
    my_resource = ckanclasses.Resource(package_id=all_resources['package_id'][i], name=all_resources['name'][i], description=all_resources['description'][i], upload=all_resources['upload'][i])
    try:
        my_resource.create()
        print('Successfully uploaded %s' % all_resources['name'][i])
    except:
        print('Failed to upload %s' % all_resources['name'][i])