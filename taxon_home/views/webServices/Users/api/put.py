import taxon_home.views.util.ErrorConstants as Errors
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Updates the given key with the update parameters
        
        @param tagKey: The tag's key to update or the tag itself
        @param updateParams: A dictionary of the new parameters for the tag to be changed
        @isKey: Indicates whether the input tagKey is actually a key or not
    '''    
    @transaction.commit_on_success 
    def updateTag(self, userId, userName, password, email, isKey=True):
        metadata = WebServiceObject()

        try:
            if (isKey):
                user = User.objects.get(pk__exact=userId)
            else:
                tag = userId
        except Exception:
            raise Errors.INTERNAL_ERROR
            
        authenticated = True

        if user.is_authenticated() or user.is_staff:
            authenticated = True
        else:
            authenticated = False

        if not authenticated:
            raise Errors.AUTHENTICATION

        if userName:
            user.username = userName

        if password:
            hashed_password = make_password(password)
            user.password = hashed_password

        if email:
            user.email = email

        try:
            user.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        metadata.limitFields(self.fields)
                
        # add new tag to response for success
        metadata.put('Status', 'Success! Following is the piece of updated information.')
        metadata.put('username', userName)
        metadata.put('password', password)
        metadata.put('email', email)
        metadata.put('is_active', user.is_active)
        
        return metadata
