
from django.contrib import admin
from django.urls import path
from mainApp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('managerConfig/', managerConfig),
    path('agentConfig/', agentConfig),
    path('jugando/', partidaEnCurso),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
