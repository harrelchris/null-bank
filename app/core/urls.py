from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("public.urls"), name="public"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("accounts.urls"), name="accounts"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("users.urls"), name="users"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
