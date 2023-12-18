from rest_framework import generics
from .models import Profile
from .pagination import ProfileAPIPagination
from .serializers import ProfileSerializer


class APIProfile(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfileAPIPagination
