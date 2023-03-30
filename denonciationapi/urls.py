
from django.contrib import admin
from django.urls import path,include


from rest_framework import permissions
from drf_yasg.views import get_schema_view

from drf_yasg import openapi


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

#-----------------------------------------------------#
#                   SWAGGER CONFIGURATION             #
#-----------------------------------------------------#
schema_view = get_schema_view(
   openapi.Info(
      title="Denunciation API",
      default_version='v1',
      description="Allegation Denunciation API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="yaomariussodokin@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

        #-----------------------------------------------------#
        #                   SWAGGER ROUTER                    #
        #-----------------------------------------------------#

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   # YOUR PATTERNS
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    #path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        #-----------------------------------------------------#
        #                   AUTHENTICATION ROUTER             #
        #-----------------------------------------------------#
        path('auth/', include('authentication.urls')),


        #-----------------------------------------------------#
        #                   COMMISSION  ROUTER                #
        #-----------------------------------------------------#
        path('deno/', include('denonciationapp.urls')),

        path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()