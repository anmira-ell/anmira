from django.urls import path
from .views.old_views import (  # Импорт старых функций
    get_servers,
    update_server,
    delete_server,
    create_service,
    update_service,
    delete_service,
    get_tunnel_token,
    get_other_servers,
    get_certificat
)
from .views import (  # Импорт новых API-классов
    ServerWizardAPI,
    CloudflareStatusAPI,
    ServiceSetupAPI
)

urlpatterns = [
    path('', get_servers, name='all_servers'),
    #path('create/', create_server, name='create_server'),
    path('<str:server_id>/update/', update_server, name='update_server'),
    path('<str:server_id>/delete/', delete_server, name='delete_server'),
    path('<str:server_id>/addservice/', create_service, name='create_service'),
    path('service/<str:service_id>/update/', update_service, name='update_service'),
    path('service/<str:service_id>/delete/', delete_service, name='delete_service'),
    path('get_token/<uuid:server_id>/', get_tunnel_token, name='get_server_token'),
    path('other/', get_other_servers, name='all_servers_other'),
    path('get_certificat/', get_certificat, name='get_certificat'),
    path('api/wizard/create/', ServerWizardAPI.as_view(), name='server-wizard-create'),
    path('api/cloudflare/status/', CloudflareStatusAPI.as_view(), name='cloudflare-status'),
    path('api/wizard/<uuid:server_id>/services/', ServiceSetupAPI.as_view(), name='server-wizard-services'),