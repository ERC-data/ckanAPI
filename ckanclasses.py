# -*- coding: utf-8 -*-
"""
This script defines classes to use with ckanapi for data management
"""

from ckanapi import RemoteCKAN, NotAuthorized

class CkanBase(object):
    """
    A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as  input
    
    Attributes:
        key, value pairs or keyword arguements passed to the object during instance initiation
    
    Methods:
        properties: a dict of key value pairs passed with which the instance was initiated
        keys: keys used in properties
        values: values used in properties
        
    Call CkanKeys.organisation for a list of all properties.
    """

    def __init__(self, items=(), **kws):
        attrs = dict(items)
        attrs.update(kws)
        
        required_attrs = ('name')
        if any([name in attrs for name in required_attrs]):
            raise ValueError('You have not specified the required properties')
        
        for key, value in attrs.items():
            setattr(self, key, value)
        
    def properties(self):        
        return self.__dict__
        
    def keys(self):
        return self.__dict__.keys()
        
    def values(self):    
        return self.__dict__.values()

class CkanKeys(object):
    
    organisation = ['name','title','description','parent']    
    dataset = ['name', 'title', 'author', 'author_email', 'maintainer', 'maintainer_email', 'license_id', 'private', 'owner_org']
    resource = ['package_id', 'name', 'url', 'description', 'upload']  

class Organisation(CkanBase):
    """
    A CKAN organisation with the following properties:
    
    Attributes:
        name: The reference ID of the organisation as a string. Can only be lowercase letters, numbers and '-'.
        title: The title of the organisation as a string.
        description: A description of the organisation as a string (optional).
        parent: The parent organisation as a string (optional).
        
    Call CkanKeys.organisation for a list of all properties.
    
    """
    def create(self, apikey, url='http://energydata.uct.ac.za'):
            site = RemoteCKAN(url, apikey)
            try:
                site.action.organization_create(self.properties()) 
            except NotAuthorized:
                print('denied')

class Dataset(CkanBase):
    """
    Define all required parameters to identify a dataset. Datasets have the following properties:
    
    Attributes:
        name:
        title:
        author:
        author_email:
        maintainer:
        maintainer_email:
        license_id:
        private: A boolean value where 'true' is a private and 'false' a public dataset (default 'false').
        owner_org: Datasets must belong to an organsation.
        
    Call CkanKeys.dataset for a list of all properties.
    """

        
    def create(self, apikey, url='http://energydata.uct.ac.za'):
            site = RemoteCKAN(url, apikey)
            try:
                site.action.package_create(self.properties()) 
            except NotAuthorized:
                print('denied')
                
class Resource(CkanBase):
    """
    Define all required parameters to identify a data resource as part of a data set.
    
    Attributes:
        package_id:        
        name:
        url:
        description:
        upload: full path to file to upload
        
    Call CkanKeys.resource for a list of all properties.
    """ 
                
    def create(self, apikey, url='http://energydata.uct.ac.za'):
            site = RemoteCKAN(url, apikey)
            try:
                site.action.resource_create(self.properties()) 
            except NotAuthorized:
                print('denied')

#########################
organisation = dict(zip(CkanKeys.organisation, vals))    
pd.Series(organisation)

class Project(Organisation):
    def __init__(self, name, title, description='', parent='ERC'):
        Organisation.__init__(self, name, title, description, parent)
        
    
#########################
        
