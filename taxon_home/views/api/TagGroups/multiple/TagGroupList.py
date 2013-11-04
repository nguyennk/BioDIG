from taxon_home.models import TagGroup
from taxon_home.serializers import TagGroupSerializer
#from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import taxon_home.views.util.Util as Util
from api.get import GetAPI
from api.post import PostAPI

from rest_framework.generics import ListCreateAPIView

class TagGroupList(ListCreateAPIView):
    serializer_class = TagGroupSerializer
    
    '''
        Gets the query set to be considered by the TagGroupList.
        Allows for query parameters on the GET & POST requests.
        
        This is used so that the default methods of the TagGroupList can be used.
    '''
    def get_queryset(self):
        query = TagGroup.objects.all()

        # read in parameters for limiting search
        lastModified = self.request.QUERY_PARAMS.get('lastModified', None)
        dateCreated = self.request.QUERY_PARAMS.get('dateCreated', None)
        user = Util.getDelimitedList(self.request.QUERY_PARAMS, 'user')
        image = Util.getDelimitedList(self.request.QUERY_PARAMS, 'image')
        name = Util.getDelimitedList(self.request.QUERY_PARAMS, 'name')

        # add permissions to query set
        if self.request.user and self.user.is_authenticated():
            if not self.user.is_staff:
                query = query.filter(isPrivate = False) | TagGroup.objects.filter(user__pk__exact=self.request.user.pk)
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

        return query