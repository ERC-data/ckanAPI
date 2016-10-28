# -*- coding: utf-8 -*-
"""
This script defines classes and functions to use with ckanapi for easy data management.

Variables:
    url
    apikey
    
Functions:
    show(name, datatype=None, apikey=None)
    search(query, datatype=None, apikey=None)

Classes & Methods:
    CkanBase(builtins.object)
        __init__(self, items=(), **kws)
        check(self)
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

from ckanapi import RemoteCKAN, NotAuthorized, ValidationError, CKANAPIError
import pandas as pd
import os

url='http://energydata.uct.ac.za'
if os.environ.get('CKAN-API-KEY') is not None:
    apikey = os.environ['CKAN-API-KEY']
else:    
    apikey = input('Paste your apikey to save it for the session. Some functions are only available to authorised users with a valid apikey.\n') or None
    if apikey is None:
        pass
    else:
        os.environ['CKAN-API-KEY'] = apikey   

def show(name, datatype=None, apikey=apikey):
    """Takes a string input and returns an existing CKAN object (organisation, dataset or resource).
    
    Arguments:
    name -- valid name or id of CKAN data object. 
            For 'resource' datatypes this must be the 36 digit 'id'.       
    datatype -- organisation, project, dataset or resource (default None)
    apikey -- a valid CKAN API key. Private datasets will only be shown to authorised API keys 
                (default None)
    """   
    d = {} #create empty dict object to contain API call results
    if datatype == None: 
        datatype = input('Is this an organisation, a project, a dataset or a resource?\n\n').lower().strip()   
    
    if datatype == 'organisation' or datatype == 'project':
        if name == 'all':
            d = RemoteCKAN(url, apikey).action.organization_list()
        else:
            try:
                d = RemoteCKAN(url, apikey).action.organization_show(id=name, include_datasets=True, 
                                                  include_groups=False, include_tags=False,  
                                                  include_followers=False, include_users=False)
            except Exception:
                print('This is neither a valid organisation nor a valid project')
    elif datatype == 'dataset':
        try:        
            d = RemoteCKAN(url, apikey).action.package_show(id=name)
        except Exception:
            print('This is not a valid dataset')
    elif datatype == 'resource':
        try:        
            d = RemoteCKAN(url, apikey).action.resource_show(id=name)
        except Exception:
            print('This is not a valid resource. Check that you are using the resource id, not the name, and try again.')
    else:
        print('Oops. Use a valid name and type a valid data type. This can be an organisation, project, dataset or resource.')
    
    if len(d) > 0: return pd.Series(d)

  
def search(query, datatype=None, apikey=apikey):
    """Takes a string input and returns search results matching existing CKAN objects (organisation, dataset, resource, user).
    
    Arguments:
    query -- a single search term 
             For 'resource' datatypes this defaults to searching the resource name. 
             Additional arguments can be added using the following syntax: 'query1 field2:query2'
             Valid resource fields can be used as field terms for the search.
    datatype -- organisation, project, dataset, resource, user (default None)
    apikey -- valid CKAN API key (default None)
              Private datasets will only be shown to authorised API keys 
    """
    # Create empty list object to contain API call results    
    d = [] 
    # Get datatype if not specified by user 
    if datatype == None: datatype = input('Are you looking for an organisation, project, dataset, resource or user?\n\n').lower().strip()    
    # Check for datatype organisation or project
    if datatype == 'organisation' or datatype == 'project':   
        d = RemoteCKAN(url, apikey).action.organization_autocomplete(q=query)
    # Check for dataytpe dataset
    elif datatype == 'dataset': 
        resources = RemoteCKAN(url, apikey).action.package_search(q=query)['results']
        for r in range(len(resources)):
            d.append({k : resources[r][k] for k in ('name','title')})        
    # Check for datatype resource
    elif datatype == 'resource': 
        query = ''.join(['name:', query])
        resources = RemoteCKAN(url, apikey).action.resource_search(query=query.split(" "))['results']
        for r in range(len(resources)):
            d.append({k : resources[r][k] for k in                  ('description','format','id','last_modified','name','package_id','revision_id')})
    # Check for datatype user
    elif datatype == 'user': 
        d = RemoteCKAN(url, apikey).action.user_autocomplete(q=query)
    else:
        print('Please try a different search query and type a valid data type. This can be an organisation, project, dataset, resource or user.\n')
    # Format results dataframe to be returned   
    if len(d) == 0:
        print('Cannot find %s for this search term' % datatype)
    elif len(d[0]) > len(d) > 0: 
        return(pd.DataFrame(d).T)
    elif len(d) > 0:
        return(pd.DataFrame(d))
        
def new_user(username, email=None, fullname=None, apikey=apikey):
    s = search(username, 'user')    
    if s is None:
        while email is None:            
            email = input('Enter new user\'s email address:\n') or None
        while fullname is None:
            fullname = input('Enter new user\'s full name:\n') or None            
        d = dict(name=username.lower().strip(), email=email, password='I love data', fullname=fullname) 
        try:
            RemoteCKAN(url, apikey).action.user_create(**d)
            return(s)
        except NotAuthorized:
            print('\nDenied. Check your apikey.')
    else:
        print('This user already exists\n', s)        


class CkanBase(object):
    """A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as input
    
    ATTRIBUTES:
        key, value pairs or keyword arguements passed to the object during instance initiation
    
    To see all attributes, use vars(object)
    """
    
    def __init__(self, items=(), **kws):
        attrs = dict(items)
        attrs.update(kws)        
        for key, value in attrs.items():
            setattr(self, key, value)
            
    def check(self):    
         if all(v in vars(self) and getattr(self, v) is not None for v in self.required):
             d = {k : vars(self).get(k, None) for k in self.attributes}
             return(pd.Series(d))
         else:
             raise ValueError('You have not specified the required attributes')     


class Organisation(CkanBase):
    """A CKAN organisation with the following attributes:
    
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
    """       
    attributes = ('name', 'title', 'parent', 'description', 'image_url') # define API parameters allowed in function call
    required = ('name',)
            
    def create(self, apikey=apikey):
        d = self.check() # check that organisation contains all required attributes and only options
        try:
            RemoteCKAN(url, apikey).action.organization_create(**d) # make CKAN API call
            return(show(self.name, 'organisation'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised
           
    def add_user(self, username, role, apikey=apikey):
        d = dict(id=self.name, username=username, role=role)
        try:
            RemoteCKAN(url, apikey).action.organization_member_create(**d)
        except ValidationError:
            print('\nUser does not exist. Create new_user() and try again.')
        except NotAuthorized:
            print('\nDenied. Check your apikey.')
        else:
            print('Added %s to %s' % (username, self.name))
                       
    def update(self, apikey=apikey): #require ID!!!!!!
        d = self.check()        
        try:
            RemoteCKAN(url, apikey).action.organization_patch(**d) # make CKAN API call
            return(show(self.name, 'organisation'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised


class Dataset(CkanBase):
    """
    Define all required parameters to identify a dataset. Datasets have the following attributes:
    
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
        
    Call CkanKeys.dataset for a list of default attributes.
    """        

    attributes = ('name', 'title', 'author', 'author_email', 'maintainer', 'maintainer_email', 'license_id', 'private', 'owner_org') # define API parameters allowed in function call
    required = ('name',)    
    
    def create(self, apikey=apikey):
        d = self.check()
        try:
            RemoteCKAN(url, apikey).action.package_create(**d)  # make CKAN API call
            return(show(self.name, 'dataset'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised
                            
    def update(self, apikey=apikey):
        d = self.check()    
        try:
            RemoteCKAN(url, apikey).action.package_patch(**d)  # make CKAN API call
            return(show(self.name, 'dataset'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised
        
                
class Resource(CkanBase):
    """
    Define all required parameters to identify a data resource as part of a data set.
    
    Attributes:
        package_id:        
        name:
        url:
        description:
        upload: full path to file to upload
        
    Call CkanKeys.resource for a list of all attributes.
    """ 
    
    attributes = ('package_id', 'name', 'url', 'description', 'upload')  # define API parameters allowed in function call
    required = ('package_id', 'name')
            
    def create(self, apikey=apikey):
        if not hasattr(self, 'url'):
            setattr(self, 'url', 'dummy-url')
        if  hasattr(self, 'upload'):
            setattr(self, 'upload', open(self.upload, 'rb'))
        d = self.check()        
        try:
            new_resource = RemoteCKAN(url, apikey).action.resource_create(**d)  # make CKAN API call
            setattr(self, 'id', new_resource['id'])             
            return(show(self.id, 'resource'))
        except NotAuthorized:
            #return('Denied. Check your apikey.')            
            print('Denied. Check your apikey.') # print 'denied' if call not authorised
        except:
            print('Failed to create %s' % self.name)
            
    def create_view(self, title='Data', view_type='recline_view', apikey=apikey):
        d = dict(resource_id=self.id, title=title, view_type=view_type)
        RemoteCKAN(url, apikey).action.resource_view_create(**d)
