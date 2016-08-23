# -*- coding: utf-8 -*-
"""
This script defines classes to use with ckanapi for data management
"""

class DataSet(object):
    """Define all required parameters to identify a dataset."""
    def __init__(self, name, title, author=None, maintainer=None, license_id = "Creative Commons Attribution"):
        self.name = name
        self.title = title
        self.author = author
        self.maintainer = maintainer
        
class DataResource(object):
    """Define all required parameters to identify a data resource as part of a data set.""" 
    def __init__(self, dataset_id, url, description=None, name, upload=None):
        self.package_id = dataset_id
        self.url = url
        self.description = descriptionUCTERC
        