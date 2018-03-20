deploy_env = os.environ.get('DEPLOYMENT_ENVIRONMENT', '')
if deploy_env == 'production':
    from .production import *
elif deploy_env == 'staging':
    try:
        from .production import *
    except ImportError:
        pass
else:
    try:
        from .local import *
    except ImportError:
        pass
