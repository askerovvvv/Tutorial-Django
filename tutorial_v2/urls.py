"""tutorial_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from account.views import RegisterApiView

schema_view = get_schema_view(
    openapi.Info(
        title='Python18 Tutorial_v2 project',
        description='Tutorial_v2',
        default_version='v2',
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('lesson/', include('lesson.urls')),
    path('course/', include('course.urls')),
    path('account/', include('account.urls')),
    path('swagger/', schema_view.with_ui('swagger'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.urls import include, path
if settings.DEBUG:
    urlpatterns = [
        # ...
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns