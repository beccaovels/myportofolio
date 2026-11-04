from rest_framework.permissions import BasePermission, SAFE_METHODS

EDITOR_GROUP = "Editor"


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Anyone may read; only the portfolio owner (superuser) may write.

    Not IsAuthenticatedOrReadOnly (every logged-in user could write) and
    not IsAdminUser (that checks is_staff, our owner rule is is_superuser).
    """

    message = "Only the portfolio owner can change experiences."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Assignment 4 roles carried over to the API.

    Anyone may read, Editors may also update (PUT/PATCH), and only the
    owner may create (POST) or delete (DELETE).
    """

    message = "Only the portfolio owner or an Editor can change skills."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name=EDITOR_GROUP).exists()
        )
