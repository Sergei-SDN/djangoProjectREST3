from rest_framework import viewsets, permissions
from .models import User
from .permissions import IsOwnerOrReadOnlyProfile
from .serializers import UserProfileSerializer, UserProfilePublicSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyProfile]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        elif self.request.method == 'PATCH' or self.request.method == 'PUT':
            return UserProfilePublicSerializer

    def get_object(self):
        return self.request.user
