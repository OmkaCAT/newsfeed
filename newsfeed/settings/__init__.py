from .base import *


SERVER = os.getenv('DEPLOYMENT_ENVIRONMENT')
if SERVER == 'production':
    from .production import *
else:
    from .local import *
