
from django.contrib import admin
from django.urls import path
from mainApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='pygomas/', permanent=False)),
    path('admin/', admin.site.urls),
    path('pygomas/', home),
    path('pygomas/menu/', menu),
    path('pygomas/createConfig/', crearConfig),
    path('pygomas/selectConfig/', selectConfig),
    path('pygomas/menu/agentConfig', agentConfig),
    path('pygomas/menu/launcher/', launcher),
    path('pygomas/menu/mapEditor', createMap),
    path('pygomas/menu/managerConfig', managerConfig),
    path('i18n/setlang/', change_language, name='change_language'),
    path('pygomas/menu/onlinemode', onlinemode),
    path('pygomas/menu/onlinemode/sendManager', sendManager),
    path('pygomas/menu/onlinemode/sendSoldier', sendSoldier),
    path('pygomas/menu/onlinemode/sendRender', sendRender),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
