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

from ckanapi import RemoteCKAN, NotAuthorized
import pandas as pd

url='http://energydata.uct.ac.za'
apikey = input('Paste your apikey to save it for the session\n\n') or None  

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
            print('This is not a valid resource')
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
        try:
            d = RemoteCKAN(url, apikey).action.organization_autocomplete(q=query)
        except Exception:
            print('No organisation or project exists for this search term')

# Check for dataytpe dataset
    elif datatype == 'dataset': 
        try:
            d = RemoteCKAN(url, apikey).action.package_autocomplete(q=query)
            for i in d: i.pop('match_displayed') #remove match_displayed:value pair from dicts
        except Exception:
            print('No dataset exists for this search term')

# Check for datatype resource
    elif datatype == 'resource': 
        try:
            query = ''.join(['name:', query])
            resources = RemoteCKAN(url, apikey).action.resource_search(query=query.split(" "))['results']
            for r in range(len(resources)):
                d.append({k : resources[r][k] for k in ('description','format','id','last_modified','name','package_id','revision_id')})
        except Exception:
            print('No resource exists for this search term')

# Check for datatype user
    elif datatype == 'user': 
        try:
            users = RemoteCKAN(url, apikey).action.user_list(q=query)
            for u in range(len(users)):
                d.append({'username':users[u]['name'], 'fullname':users[u]['fullname']})
        except Exception:
            print('Cannot find user for this search term') 
    else:
        print('Please try a different search query and type a valid data type. This can be an organisation, project, dataset or resource.')

# Format results dataframe to be returned   
    if len(d[0]) > len(d) > 0: 
        return(pd.DataFrame(d).T)
    elif len(d) > 0:
        return(pd.DataFrame(d))
        
def new_user(username, email=None, fullname=None, apikey=apikey):
    while email is None:            
        email = input('Enter new user\'s email address:\n') or None
    while fullname is None:
        fullname = input('Enter new user\'s full name:\n') or None            
    d = dict(name=username.lower().strip(), email=email, password='I love data', fullname=fullname)
    try:
        RemoteCKAN(url, apikey).action.user_create(**d)
    except NotAuthorized:
        print('Denied. Check your apikey.')


class CkanBase(object):
    """A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as input
    
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
            
    def check(self):    
         if all(v in vars(self) and getattr(self, v) is not None for v in self.required):
             d = {k : vars(self).get(k, None) for k in self.options}
             return(d)
         else:
             raise ValueError('You have not specified the required properties')     


class Organisation(CkanBase):
    """A CKAN organisation with the following properties:
    
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
    options = ('name', 'title', 'parent', 'description', 'image_url') # define API parameters allowed in function call
    required = ('name',)
            
    def create(self, apikey=apikey):
        d = self.check() # check that organisation contains all required attributes and only options
        try:
            RemoteCKAN(url, apikey).action.organization_create(**d) # make CKAN API call
            return(show(self.name, 'organisation'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised
           
    def add_user(self, username, role, apikey=apikey):
        try:
            RemoteCKAN(url, apikey).action.user_search(id=username) ######CHECK API CALL!!
        except None:
            print('User does not exist. Let\'s create her.')
            new_user(username)
        if self.name is not None:
            d = dict(id=self.name, username=username, role=role)
        else:
            raise ValueError('You have not specified the required properties') 
        try:
            RemoteCKAN(url, apikey).action.organization_member_create(**d)
        except NotAuthorized:
            print('Denied. Check your apikey.')
                       
    def update(self, apikey=apikey): #require ID!!!!!!
        d = self.check()        
        try:
            RemoteCKAN(url, apikey).action.organization_patch(**d) # make CKAN API call
            return(show(self.name, 'organisation'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised


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

    options = ('name', 'title', 'author', 'author_email', 'maintainer', 'maintainer_email', 'license_id', 'private', 'owner_org') # define API parameters allowed in function call
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
        
    Call CkanKeys.resource for a list of all properties.
    """ 
    
    options = ('package_id', 'name', 'url', 'description', 'upload')  # define API parameters allowed in function call
    required = ('name',)
            
    def create(self, apikey=apikey):
        d = self.check()        
        try:
            RemoteCKAN(url, apikey).action.resource_create(**d)  # make CKAN API call
            return(show(self.name, 'resource'))
        except NotAuthorized:
            print('Denied. Check your apikey.') # print 'denied' if call not authorised

#########################
#organisation = dict(zip(CkanKeys.organisation, vals))    
#pd.Series(organisation)

