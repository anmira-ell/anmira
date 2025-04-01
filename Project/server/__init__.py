from .old_views import *
from .create_service_api import (
    ServerWizardAPI,
    CloudflareStatusAPI,
    ServiceSetupAPI
)
try:
    from .views import *
except ImportError:
    pass  # Для совместимости с предыдущими версиями

from .old_views import *