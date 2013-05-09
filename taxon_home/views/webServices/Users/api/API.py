import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
import simplejson as json
from get import GetAPI
from post import PostAPI
from put import PutAPI
from delete import DeleteAPI
import re

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
'''
def getUser(request):
    # read in crucial parameters
    userId = request.GET.get('id', None)
    if not userId:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)
        
    # the key for lookup and the image it is attached to
    return getAPI.getUser(userId)

'''
    Updates the tag information as posted and returns the newly updated tag information
    
    @param request: Django Request object to be used to parse the query
'''
def updateUser(request):
    # read in the crucial parameters
    userId = request.PUT.get('id', None)
    if not userId:
        raise Errors.MISSING_PARAMETER.setCustom('id')

    userName = request.PUT.get('username', None)
    if not userName:
        raise Errors.MISSING_PARAMETER.setCustom('username')

    password = request.PUT.get('password', None)
    if not password:
        raise Errors.MISSING_PARAMETER.setCustom('password')

    email = request.PUT.get('email', None)
    if not email:
        raise Errors.MISSING_PARAMETER.setCustom('email')
    elif not re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',email):
        raise Errors.INTERNAL_ERROR

    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    return putAPI.updateTag(userId, userName, password, email)

'''
    Creates a new gene link and returns the representation of the newly created gene link.
    
    @param request: Django Request object to be used to parse the query
'''
def createUser(request):

    # get the username
    userName = request.POST.get('username', None)
    if not userName:
        raise Errors.NO_USER_NAME

    # get password
    password = request.POST.get('password', None)
    if not password:
        raise Errors.INTERNAL_ERROR

    # get email
    email = request.POST.get('email', None)
    if not email:
        raise Errors.INTERNAL_ERROR
    elif not re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',email):
        raise Errors.INTERNAL_ERROR
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.POST, 'fields')
        
    postAPI = PostAPI(request.user, fields)
    return postAPI.createUser(userName, password, email)

'''
    Deletes a tag and returns the information for the tag that was deleted
'''
def deleteUser(request):
    userId = request.DELETE.get('id', None)
    if not userId:
        raise Errors.MISSING_PARAMETER.setCustom('id')

    #geneLinkKey = request.DELETE.get('id', None)
    
    #if not geneLinkKey:
     #   raise Errors.MISSING_PARAMETER.setCustom('id')
    
    # get optional parameter
    fields = Util.getDelimitedList(request.DELETE, 'fields')
    
    deleteAPI = DeleteAPI(request.user, fields)
    return deleteAPI.deleteUser(userId)
    
    
    
