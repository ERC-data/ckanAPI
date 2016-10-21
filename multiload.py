# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:07:46 2016

This script helps users create a new CKAN dataset and upload multiple resources to it.

@author: saintlyvi
"""

import ckanfunctions
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

#7 get upload urls from path
#8 get names from list

#9 add description to each list item
                