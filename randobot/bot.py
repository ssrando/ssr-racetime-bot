from racetime_bot import Bot

from .handler import RandoHandler
from .generator import Generator


class RandoBot(Bot):
    """
    RandoBot base class.
    """

    def __init__(self, github_token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = Generator(github_token)

    def get_handler_class(self):
        return RandoHandler

    def get_handler_kwargs(self, *args, **kwargs):
        return {
            **super().get_handler_kwargs(*args, **kwargs),
            "generator": self.generator,
        }
