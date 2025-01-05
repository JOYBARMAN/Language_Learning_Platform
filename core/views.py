from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class MeInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return self.request.user
        except User.DoesNotExist:
            raise Http404