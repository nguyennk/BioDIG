import taxon_home.views.util.ErrorConstants as Errors
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject

class GetAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the tags in the database that are private
    '''
    def getUser(self, userId, isKey=True):
        metadata = WebServiceObject()
        
        try:            
            if (isKey):
                user = User.objects.get(pk__exact=userId)
            else:
                user = userId
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_USER_NAME
        except Exception:
            raise Errors.INTERNAL_ERROR
        
        metadata.limitFields(self.fields)

        metadata.put('Status', 'Success! Following contains the required information about the user')
        metadata.put('firstname', user.first_name)
        metadata.put('lastname', user.last_name)
        metadata.put('username', user.username)
        metadata.put('email', user.email)
        metadata.put('is_active', user.is_active)

        return metadata
