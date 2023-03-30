from django.urls import path,include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', AccountUserViewset)


urlpatterns = [

    path('', include(router.urls)),

    path('', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.social.urls')),

    path('logout/', LogoutAPIView.as_view(), name="logout"),


    path('user-me/update/', CustomAdministratorViewset.as_view(), name='patch_user'),
    path('users/activation/<str:email>/<str:code>/', UserActivationView.as_view()),


]