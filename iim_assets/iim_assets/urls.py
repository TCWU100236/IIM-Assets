"""
URL configuration for iim_assets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/<int:id>', views.detail, name = 'detail-url'),
    path('asset_user/', views.asset_user, name = 'all-asset-user'),
    path("delete_asset_user/<int:userid>/", views.del_asset_user),
    path('InsertAsset/', views.InsertAsset),
    path('login/', views.login),
    path('logout/', views.logout),
    path('SystemUserInfo/', views.SystemUserInfo),
    path('', views.index, name = 'home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
