# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:07:46 2016

This script helps users create a new CKAN dataset and upload multiple resources to it.

@author: saintlyvi
"""

import ckanclasses, ckanfunctions
import pandas as pd

# Section 1: Dataset creation or selection
print('********************\nThis section helps you create or select a dataset to update.\n********************\n')
dataset_status = input('Are you creating a new dataset?\n')

if dataset_status.lower().strip() != 'no':
    dataset = ckanfunctions.new_dataset()    
else:    
    dataset = ckanfunctions.search_dataset()

# Section 2: Adding resources for upload to dataset
print('\n********************\nThis section helps you upload multiple resources to your dataset.\n********************')

#6 get list of resources in folder
(resource_folder, all_resources) = ckanfunctions.select_folder()
resource_upload = ckanfunctions.upload_files(all_resources)

#7 get upload urls from path
upload_paths = []
for r in resource_upload:
    r_path = '/'.join([resource_folder, all_resources[r]])
    upload_paths.append(r_path)

resources = pd.DataFrame({'packageid':dataset.name , 'name':all_resources, 'upload':upload_paths})

#8 get names from list

#9 add description to each list item
                