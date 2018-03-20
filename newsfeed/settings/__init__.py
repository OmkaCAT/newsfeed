from .base import *


SERVER = os.getenv('SERVER')
if SERVER == 'production':
    from .production import *
else:
    from .local import *
