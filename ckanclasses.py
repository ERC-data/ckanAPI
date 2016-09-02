# -*- coding: utf-8 -*-
"""
This script defines classes and functions to use with ckanapi for easy data management.

Variables:
    url
    
Functions:
    show(name, datatype=None, apikey=None)
    search(query, datatype=None, apikey=None)

Classes & Methods:
    CkanBase(builtins.object)
        __init__(self, items=(), **kws)
    Organisation(CkanBase)
        create(self, apikey)
        add_member(self, apikey, username, role)
        update(self, apikey)
    Dataset(CkanBase)
        create(self, apikey)
        update(self, apikey)
    Resource(CkanBase)
        create(self, apikey)
"""

from ckanapi import RemoteCKAN, NotAuthorized
import pandas as pd

url='http://energydata.uct.ac.za'

def show(name, datatype=None, apikey=None ):
    """Takes a string input and returns an existing CKAN object.
    
    Arguments:
    name -- valid name or id of CKAN data object. 
            For 'resource' datatypes this must be the 36 digit 'id'.       
    datatype -- organisation, dataset or resource (default None)
    apikey -- a valid CKAN API key. Private datasets will only be shown to authorised API keys 
                (default None)
    """
    site = RemoteCKAN(url, apikey)     
    d = {} #create empty dict object to contain API call results
    if datatype == None: 
        datatype = input('Is this an organisation, a dataset or a resource?\n\n').lower().strip()   
    
    if datatype == 'organisation':#any(['organisation', 'project']):
        try:
            d = site.action.organization_show(id=name, include_datasets=True, 
                                              include_groups=False, include_tags=False,  
                                              include_followers=False, include_users=False)
        except Exception:
            print('This is neither a valid organisation nor a valid project')
    elif datatype == 'dataset':
        try:        
            d = site.action.package_show(id=name)
        except Exception:
            print('This is not a valid dataset')
    elif datatype == 'resource':
        try:        
            d = site.action.resource_show(id=name)
        except Exception:
            print('This is not a valid resource')
    else:
        print('Oops. Use a valid name and type a valid data type. This can be an organisation, dataset or resource.')
    
    if len(d) > 0: return pd.Series(d)

  
def search(query, datatype=None, apikey=None):
    """Takes a string input and returns search results matching existing CKAN objects (organisation, dataset or resource).
    
    Arguments:
    query -- a single search term 
             For 'resource' datatypes this defaults to searching the resource name. 
             Additional arguments can be added using the following syntax: 'query1 field2:query2'
             Valid resource fields can be used as field terms for the search.
    datatype -- organisation, dataset or resource (default None)
    apikey -- valid CKAN API key (default None)
              Private datasets will only be shown to authorised API keys 
    """
    site = RemoteCKAN(url, apikey)
    d = [] #create empty list object to contain API call results
    if datatype == None: datatype = input('Are you looking for an organisation, a dataset or a resource?\n\n').lower().strip()    

    if datatype == 'organisation':#any(['organisation', 'project']):    
        try:
            d = site.action.organization_autocomplete(q=query)
        except Exception:
            print('No organisation or project exists for this search term')
    elif datatype == 'dataset': 
        try:
            d = site.action.package_autocomplete(q=query)
            for i in d: i.pop('match_displayed') #remove match_displayed:value pair from dicts
        except Exception:
            print('No dataset exists for this search term')
    elif datatype == 'resource': 
        try:
            query = ''.join(['name:', query])
            d = site.action.resource_search(query=query.split(" "))['results']
        except Exception:
            print('No resource exists for this search term')        
    else:
        print('Please try a different search query and type a valid data type. This can be an organisation, dataset or resource.')
   
    if len(d) > 0: return pd.DataFrame(d).T


class CkanBase(object):
    """
    A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as input
    
    ATTRIBUTES:
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
    
    Options:
    name: The reference ID of the organisation as a string. 
            Can only be lowercase letters, numbers and '-'.
    title: The title of the organisation as a string.
    description: A description of the organisation as a string (optional).
    parent: The parent organisation as a string (optional).
    image_url: URL to an image on the internet.
        
    Methods:
    create: Requires attribute 'name' (string) and argument 'apikey'. 
            Optional arguments 'title', 'parent', 'description', 'image_url'
    member_add: Requires attribute 'name' (string) and arguments 'apikey', 
            'username' (string), 'role' (string) one of ['member', 'editor', 'admin']
    update:         
        
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

