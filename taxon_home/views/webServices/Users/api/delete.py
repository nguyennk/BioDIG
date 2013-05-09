import taxon_home.views.util.ErrorConstants as Errors
from django.contrib.auth.models import User
from taxon_home.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class DeleteAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the tags in the database that are private
    '''
    @transaction.commit_on_success 
    def deleteUser(self, userId):
        metadata = WebServiceObject()
        
        try:
            user = User.objects.get(pk__exact=userId)
            user_profile = UserProfile.objects.get(user_id=userId)
        except Exception:
            raise Errors.INTERNAL_ERROR

        authenticated = True

        if user.is_authenticated() or user.is_staff:
            authenticated = True
        else:
            authenticated = False

        if not authenticated:
            raise Errors.AUTHENTICATION

        metadata.limitFields(self.fields)
        
        metadata.put('Status','Success! Following is the piece of deleted information.')
        metadata.put('username', user.username)
        metadata.put('email',user.email)
        metadata.put('is_active', user.is_active)

        try:
            user_profile.delete()
            user.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))

        return metadata
