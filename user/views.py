from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from .permissions import IsAdmin, IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_permissions(self):
        if self.action == 'register':
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'destroy','change_password']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", "Use the /users/register/ endpoint to create users.")
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user or request.user.role == 'admin':
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed("DELETE", "You can only deactivate your own account.")

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        """Public registration endpoint"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsOwnerOrAdmin])
    def change_password(self, request, username=None):
        """Change user password"""
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAdmin])
    def reactivate(self, request, username=None):
        """Reactivate a deactivated user"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)
