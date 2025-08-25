from rest_framework import generics
# from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer

class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    
    def get_queryset(self):
        # You can add version-specific logic here
        version = self.request.version
        
        if version == 'v1':
            # v1 specific queryset logic
            return Location.objects.all()
        # For future versions, add elif blocks
        # elif version == 'v2':
        #     return Location.objects.filter(active=True)
        
        return Location.objects.all()
    
    def list(self, request, *args, **kwargs):
        # Add version information to response if needed
        response = super().list(request, *args, **kwargs)
        response.data['api_version'] = request.version
        return response

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # Add version information to response if needed
        response = super().retrieve(request, *args, **kwargs)
        response.data['api_version'] = request.version
        return response