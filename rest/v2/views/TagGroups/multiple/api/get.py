import base.util.ErrorConstants as Errors
from base.models import TagGroup
from django.core.exceptions import ObjectDoesNotExist
from base.renderEngine.WebServiceObject import WebServiceArray, LimitDict
from base.serializers import TagGroupSerializer
import base.util.Util as Util

class GetAPI:
    
    def __init__(self, limit=10, offset=0, user=None, fields=None, unlimited=False):
        self.limit = limit
        self.offset = offset
        self.unlimited = unlimited
        self.user = user
        self.fields = fields
    
    '''
        
    '''
    def getTagGroups(self, name, image, user, lastModified, dateCreated):
        metadata = WebServiceArray()
        
        query = TagGroup.objects.all()
        
        # add permissions to query
        if self.user and self.user.is_authenticated():
            if not self.user.is_staff:
                query = query.filter(isPrivate = False) | TagGroup.objects.filter(user__pk__exact=self.user.pk)
        else:
            query = query.filter(isPrivate=False)
        
        # if a name was given then we will filter by it
        if name: query = query.filter(name__in=name)
        
        if image: query = query.filter(picture__pk__in=image)
            
        if user: query = query.filter(user__pk__in=user)
            
        if lastModified:
            keyArgs = Util.getFilterByDate(lastModified, 'lastModified')
            query = query.filter(**keyArgs)
            
        if dateCreated:
            keyArgs = Util.getFilterByDate(dateCreated, 'dateCreated')
            query = query.filter(**keyArgs)
            
        if self.unlimited:
            query = query[self.offset:]
        else:
            query = query[self.offset : self.offset+self.limit]
        
        for group in query:
            metadata.put(LimitDict(self.fields, TagGroupSerializer(group).data))
        
        return metadata
    
    
