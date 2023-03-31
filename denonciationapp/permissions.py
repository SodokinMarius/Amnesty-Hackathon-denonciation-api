from rest_framework import permissions


class isSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if request.user:
            return (obj.administrator.is_admin
                    and obj.administrator.is_staff
                    and obj.administrator.is_superuser )
        else :
            return False