"""virtualpaintproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from virtualpaint.views import index, index_select, vp_draw, delete_colors, how_to_paint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('index_select/', index_select, name='index_select'),
    path('delete_colors/', delete_colors, name='delete_colors'),
    path('vp_draw/', vp_draw, name='vp_draw'),
    path('how_to_paint/', how_to_paint, name='how_to_paint'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)