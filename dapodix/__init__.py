from .version import __version__, __dapodik_version__  # NOQA
from .click_context import ContextObject, ClickContext
from .peserta_didik import RegistrasiPesertaDidikCommand

__all__ = ["ClickContext", "ContextObject", "RegistrasiPesertaDidikCommand"]
