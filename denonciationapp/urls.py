from django.urls import path,include
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()


router.register('denonciations',DenonciationViewSet)

router.register('categories',CategoryViewSet)

router.register('denonciators',DenonciatorViewSet)

router.register('teams',TeamViewSet)

router.register('steps',StepViewSet)

router.register('actors',ActorViewSet)

router.register('publications',PublicationViewSet)

router.register('petitions',PetitionViewSet)











urlpatterns = router.urls