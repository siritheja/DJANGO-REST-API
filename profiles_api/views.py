from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from . import serializers, models
from rest_framework.authentication import TokenAuthentication 
from . import permission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

class HelloApiView(APIView):
    """ Test API View. This creates a class based apiview to define the logic for our project"""
    serializer_class = serializers.HelloSerializer
    def get(self,request,format=None):
        """ returns a list of api view feature """
        an_apiview = [
            'uses HTTP methods as function (get,post,patch,put,delete)',
            'Is similar to a traditional sjango view',
            'gives you most control over your application logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message':'Hello!','an_apiview':an_apiview})
    def post(self,request):
        """ create hello request with our name """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message':message})
        else :
            return Response(
                    serializer.errors ,
                    status = status.HTTP_400_BAD_REQUEST
                    )
    
    def put(self,request,pk=None):
        """ Handling updating a object. Normally u will do update for a primary key of a request ie.., 
        id if we dont want the primary key then put pk =None  """
        return Response({'method':'PUT'})

    def patch(self,request,pk=None):
        """ update partially .
            If u have first and last name and apply patch for last name then that only will be update whereas 
            in pu request remove first name as only last name is passed for updating entire object """
        return Response({'method':'PATCH'})
    
    def delete(self,request,pk=None):
        """ delete an object in data base """
        return Response({'method':'DELETE'})


class HelloViewSets(viewsets.ViewSet):
    """ Test API View sets """
    serializer_class = serializers.HelloSerializer
    def list(self,request):
        an_viewset = [
            'uses HTTP methods as function (create,destroy,update,partial_update)',
            'automatically maps to urls using routers',
            'Provides more functionality with less code',
        ]
        return Response({'message':'Hello!','an_viewset':an_viewset})	
    
    def create(self,request):
        """ Create a new hello message """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request,pk=None):
        """ geting an object by its id """
        return Response({'http_method':'GET'})

    def update(self,request,pk=None):
        return Response({'http_method':'PUT'})

    def partial_update(self,request,pk=None):
        return Response({'http_method':'PATCH'})

    def destroy(self,request,pk=None):
        return Response({'http_method':'DELETE'})
        

class UserProfileViewset(viewsets.ModelViewSet):
    """ Handles creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends =(filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication tokens """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.UpdateOwnStatus,IsAuthenticated) 
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
