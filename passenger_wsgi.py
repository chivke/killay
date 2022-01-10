import os
import sys


def get_application():
    root_dir = os.path.dirname(__file__)
    virtual_env = os.path.join(
        root_dir, "env", 'bin', 'python'
    )
    if sys.executable != virtual_env:
        os.execl(virtual_env, virtual_env, *sys.argv)
    sys.path.insert(0, os.path.join(os.getcwd(), virtual_env, 'bin'))
    sys.path.append(os.path.join(root_dir, "killay"))
    sys.path.append(os.path.join(root_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()

application = get_application()
