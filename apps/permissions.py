from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser


class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active and request.user.is_registered


class IsGetOrLocked(BaseAuthentication):

    def __init__(self):
        self.base_auth = JWTAuthentication()

    def authenticate(self, request):
        # action olish uchun view
        view = getattr(request, "parser_context", {}).get("view", None)
        action = getattr(view, "action", None)

        # GET / list/retrieve bo'lsa authni o'chirish
        if request.method == "GET" and action in ["list", "retrieve"]:
            return None

        # boshqa requestlar uchun base authenticator ishlaydi
        return self.base_auth.authenticate(request)