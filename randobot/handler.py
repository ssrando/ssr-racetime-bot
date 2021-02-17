import asyncio
from datetime import datetime, timedelta
from racetime_bot import RaceHandler, monitor_cmd, can_monitor


class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

    STANDARD_RACE_PERMALINK = "MS44LjAAU3RhbmRhcmRSYWNlRXhhbXBsZQAXAwQATjDADAAAAAAAAAA="

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()
        self.loop_ended = False