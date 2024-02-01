from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    path('', include("products.urls")),
    path('', include("orders.urls")),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^ru/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^uz/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]+i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('accounts.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    prefix_default_language=False
)
