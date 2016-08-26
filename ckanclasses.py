# -*- coding: utf-8 -*-
"""
This script defines classes to use with ckanapi for data management
"""

from ckanapi import RemoteCKAN, NotAuthorized

class CkanBase(object):
    """
    A base class for creating CKAN data objects. CkanBase takes a list of (key,value) pairs or keyword arguments as  input
    
    ATTRIBUTES:
        url: site url; defaults to http://energydata.uct.ac.za
        key, value pairs or keyword arguements passed to the object during instance initiation
    
    METHODS:
        properties: a dict of key value pairs with which the instance was initiated
        keys: keys used in properties
        values: values used in properties
        
    Call CkanKeys.organisation for a list of default properties.
    """
    url='http://energydata.uct.ac.za'
    
    def __init__(self, items=(), **kws):
        attrs = dict(items)
        attrs.update(kws)
        required_attrs = ()
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# functions using action.create and action.patch
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def create(self, apikey, url=url):
        site = RemoteCKAN(url, apikey)
        options = ('name', 'title', 'parent', 'description', 'image_url') # define API parameters allowed in function call
        required = ('name')
        d = {k : self.properties().get(k, None) for k in options} # create a dict consisting only of permitted key:value pairs
        if all([name in d for name in required]):
            pass
        else:
            raise ValueError('You have not specified the required properties')        
        try:
            site.action.organization_create(d) # make CKAN API call
        except NotAuthorized:
            print('denied') # print 'denied' if call not authorised
            
    def member_add(self, url=url, apikey, username, role):
        site = RemoteCKAN(url, apikey)
        options = ('name')
        d = {k : self.properties().get(k, None) for k in options}
        d['id'] = d.pop('name')
        d['username'] = username
        d['role'] = role
        try:
            site.action.organization_member_create(d)
        except NotAuthorized:
            print('denied')
            
    def update(self, apikey=None, url=url):
        site = RemoteCKAN(url, apikey)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# functions using action.get
#~~~~~~~~~~~~~~~~~~~~~~~~~~~
                
    def show(self, apikey=None, url=url):
        site = RemoteCKAN(url, apikey=None)
        try:
            return site.action.organization_show(id=self.properties()['name'], include_groups=False, include_tags=False,  include_followers=False)
        except NotAuthorized:    
            print('denied')
            
    def search(query, apikey=None, url=url):
        site = RemoteCKAN(url, apikey)
        try:
            return site.action.organization_autocomplete(q=query)
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
        
    Call CkanKeys.dataset for a list of default properties.
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
        
