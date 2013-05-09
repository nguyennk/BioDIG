import taxon_home.views.util.ErrorConstants as Errors
from django.contrib.auth.models import User
from taxon_home.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate
import uuid

class PostAPI:
    
    def __init__(self, user, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Creates a new tag with the given parameters
        
        @param points: The points for a tag in an array of dictionaries
            format: [{"x" : 256, "y" : 350}, ...]
        @param description: The description for this tag
        @param color: The color array for this tag
            format: [r, g, b]
    '''   
    @transaction.commit_on_success  
    def createUser(self, userName, password, email):
        metadata = WebServiceObject()
        
        is_active=False
        hashed_password = make_password(password)

        if authenticate(username=userName,password=hashed_password) != None:
            raise Errors.INTERNAL_ERROR

        user = User(username=userName, password=hashed_password, email=email,is_active=is_active)
        try:
            user.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))

        hex_id = uuid.uuid4()
        hex_user = ''
        for i in str(userName):
            hex_user = hex_user + str(ord(i))
        activation_key = str(hex_id) + hex_user
        new_profile = UserProfile(user=user, activation_key=activation_key)
        try:
            new_profile.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))

        self.message = 'Valid credentials.Please check email for activating your account'
        url = 'localhost/activate?username=%s&activationKey=%s' %(str(userName),activation_key)
        subject, from_email, to = 'Thank you for registering with BioDIG', 'rajeswari284@gmail.com',email
        text_content = ''
        html_content = '<html><body><p>Please click the link below to activate your account</p><a href=%s>Click Here</a></body></html></p>' %(url)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        # limit metadata return
        metadata.limitFields(self.fields)
        
        # add new tag to response for success
        metadata.put('Status', 'Success! Following is the information posted to the database.')
        metadata.put('username', userName)
        metadata.put('email', email)
        metadata.put('is_active', is_active)
        
        return metadata
        
        
