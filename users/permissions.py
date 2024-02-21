from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import User


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return (
            request.user.is_authenticated and request.user
        )


class IsUserOwner(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: User):
         
        if request.user.is_employee:
            return True

        # Permite acesso se o perfil pesquisado for o próprio usuário autenticado
        if obj == request.user:
            return True

        # Não permite acesso para usuários não-employee que tentam acessar informações de outros perfis
        return False