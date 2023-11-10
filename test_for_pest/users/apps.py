from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "test_for_pest.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import test_for_pest.users.signals  # noqa: F401
        except ImportError:
            pass
