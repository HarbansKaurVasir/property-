"""
URL configuration for RestFrameWork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from data.views import GeneralInfoViewSet, PropertyViewSet, AddressViewSet, EconomicInfoViewSet, AmenityInfoViewSet, ChargeInfoViewSet,ExtraFeeViewSet,UtilityInfoViewSet,DocumentInfoViewSet,UserViewSet,UserExistsView 
from data.decorators import check_credentials

from file.views import DocumentViewSet
from django.conf import settings
from django.conf.urls.static import static


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register(r'general-info', GeneralInfoViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'address', AddressViewSet)
router.register(r'economic_info', EconomicInfoViewSet)
router.register(r'amenities', AmenityInfoViewSet)
router.register(r'charge_info', ChargeInfoViewSet)
router.register(r'extrafee', ExtraFeeViewSet)
router.register(r'utility', UtilityInfoViewSet)
router.register(r'documnet_info', DocumentInfoViewSet)
router.register(r'users', UserViewSet)


router.register(r'documents', DocumentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/login/', UserExistsView.as_view(), name='user_login'),
]
