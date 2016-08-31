# -*- coding: utf-8 -*-
"""
This script defines classes to use with ckanapi for data management
"""

from ckanapi import RemoteCKAN, NotAuthorized
import pandas as pd

url='http://energydata.uct.ac.za'

# This function shows the details of a CKAN data object (organisation, dataset or resource)
def show(name, datatype=None, apikey=None ):
    site = RemoteCKAN(url, apikey)     
    if datatype == None: 
        datatype = input('Is this an organisation, a project, a dataset or a resource?\n\n').lower().strip()
    if datatype == any(['organisation', 'project']):
        try:
            d = site.action.organization_show(id=name, include_groups=False, include_tags=False,  include_followers=False, include_users=False)
        except Exception:
            print('This is neither a valid organisation nor a valid project')
    if datatype == 'dataset':
        try:        
            d = site.action.package_show(id=name)
        except Exception:
            print('This is not a valid dataset')
    if datatype == 'resource':
        try:        
            d = site.action.resource_show(id=name)
        except Exception:
            print('This is not a valid resource')
    else:
        print('Oops. Use a valid name and type a valid data type. This can be an organisation, dataset or resource.')
    return pd.DataFrame(d)
 
# This function shows all CKAN data objects for a search term (organisation, dataset or resource)   
def search(query, datatype=None, apikey=None):
    if datatype == None: datatype = input('Are you looking for an organisation, a project, a dataset or a resource?\n\n').lower().strip()    
    site = RemoteCKAN(url, apikey)
    if datatype == any(['organisation', 'project']):    
        try:
            d = site.action.organization_autocomplete(q=query)
        except Exception:
            print('No organisation or project exists for this search term')
    if datatype == 'dataset': 
        try:
            d = site.action.package_autocomplete(q=query)
        except Exception:
            print('No dataset exists for this search term')
    if datatype == 'resource': 
        try:
            d = site.action.resource_search(query=query)
        except Exception:
            print('No resource exists for this search term')        
    else:
        print('Please try a different search query and type a valid data type. This can be an organisation, dataset or resource.')
    return pd.DataFrame(d)

class CkanBase(object):
    """
    A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as  input
    
    ATTRIBUTES:
        url: site url; defaults to http://energydata.uct.ac.za
        key, value pairs or keyword arguements passed to the object during instance initiation
    
    To see all attributes, use vars(object)
        
    Call CkanKeys.organisation for a list of default properties.
    """
    
    def __init__(self, items=(), **kws):
        attrs = dict(items)
        attrs.update(kws)        
        for key, value in attrs.items():
            setattr(self, key, value)

class CkanKeys(object):
    
    organisation = ('name', 'title', 'parent', 'description', 'image_url')    
    dataset = ('name', 'title', 'author', 'author_email', 'maintainer', 'maintainer_email', 'license_id', 'private', 'owner_org')
    resource = ('package_id', 'name', 'url', 'description', 'upload')  

class Organisation(CkanBase):
    """
    A CKAN organisation with the following properties:
    
    ATTRIBUTES:
        name: The reference ID of the organisation as a string. Can only be lowercase letters, numbers and '-'.
        title: The title of the organisation as a string.
        description: A description of the organisation as a string (optional).
        parent: The parent organisation as a string (optional).
        image_url: URL to an image on the internet.
        
    METHODS:
        create: Requires attribute 'name' (string) and argument 'apikey'. Optional arguments 'title', 'parent', 'description', 'image_url'
        member_add: Requires attribute 'name' (string) and arguments 'apikey', 'username' (string), 'role' (string) one of ['member', 'editor', 'admin']
        update:         
        show: requires keywords 'name', '', ''
        search:  requires query string
        
    Call CkanKeys.organisation for a list of default properties.
    """       
# functions using action.create and action.patch    
    def create(self, apikey):
        site = RemoteCKAN(url, apikey)
        options = ('name', 'title', 'parent', 'description', 'image_url') # define API parameters allowed in function call
        required = ('name')
        d = {k : vars(self).get(k, None) for k in options} # create a dict consisting only of permitted key:value pairs
        if all([name in d for name in required]):
            pass
        else:
            raise ValueError('You have not specified the required properties')        
        try:
            site.action.organization_create(d) # make CKAN API call
        except NotAuthorized:
            print('denied') # print 'denied' if call not authorised
            
    def add_member(self, apikey, username, role):
        site = RemoteCKAN(url, apikey)
        options = ('name')
        d = {k : vars(self).get(k, None) for k in options}
        d['id'] = d.pop('name')
        d['username'] = username
        d['role'] = role
        try:
            site.action.organization_member_create(d)
        except NotAuthorized:
            print('denied')
            
    def update(self, apikey=None):
        site = RemoteCKAN(url, apikey)

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
        
    Call CkanKeys.dataset for a list of default properties.
    """        
    def create(self, apikey):
            site = RemoteCKAN(url, apikey)
            try:
                site.action.package_create(vars(self)) 
            except NotAuthorized:
                print('denied')
                
    def update():
        site.action.package_patch(d)
        
                
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
                
    def create(self, apikey):
            site = RemoteCKAN(url, apikey)
            try:
                site.action.resource_create(self.properties()) 
            except NotAuthorized:
                print('denied')

#########################
#organisation = dict(zip(CkanKeys.organisation, vals))    
#pd.Series(organisation)

