"""Application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import admin_tools
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static, serve
from django.contrib import admin
import debug_toolbar
from django.urls import include, path
from django.views.static import serve as mediaserve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('users.urls')),
    path('api/junior/', include('junior_group.urls')),
    path('api/middle/', include('middle_group.urls')),
    path('api/senior/', include('senior_group.urls')),
    path('api/preparatory/', include('preparatory_group.urls')),
]

if not settings.DEBUG:
    urlpatterns += [
        url(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
            mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]
