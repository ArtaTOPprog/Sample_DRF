from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    owner_field = "owner"

    def has_object_permission(self, request, view, obj):
        return getattr(obj, getattr(view, "owner_field", self.owner_field)) == request.user


class IsOwnerOrReadOnly(IsOwner):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)
