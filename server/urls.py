from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from serverrequest.views import *
  
urlpatterns = [ 
    path('', image_as_base64),
    path('base64',image_as_base64, name='base64'),
] 
  
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 

