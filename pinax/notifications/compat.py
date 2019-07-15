try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote  # noqa

from threading import get_ident

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa
