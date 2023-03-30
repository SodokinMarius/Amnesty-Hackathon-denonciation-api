from django.urls import path,include
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()


router.register('denonciations',DenonciationViewSet)


urlpatterns = router.urls