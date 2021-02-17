import asyncio
from datetime import datetime, timedelta
from racetime_bot import RaceHandler, monitor_cmd, can_monitor


class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

    STANDARD_RACE_PERMALINK = "JQEABAS+AA=="

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()
        self.loop_ended = False

    async def begin(self):
        self.state["permalink"] = self.STANDARD_RACE_PERMALINK
        
    async def ex_francais(self, args, message):
        self.state["use_french"] = True
        await self.send_message("Bot responses will now also be in French.")
        await self.send_message("Translate 'Bot responses will now also be in French.' to French.")

    async def ex_permalink(self, args, message):
        if not self.state.get("permalink_available"):
            await self.send_message("There is no permalink! Please use !rollseed to get a permalink")
            if self.state.get("use_french"):
                await self.send_message("Translate 'There is no permalink! Please use !rollseed to get a permalink' to French")
            return
        permalink = self.state.get("permalink")
        await self.send_message(f"The permalink is: {permalink}")
        if self.state.get("use_french"):
            await self.send_message(f"Translate 'The permalink is: {permalink}' to French.")
            
    @monitor_cmd
    async def ex_lock(self, args, message):
        self.state["locked"] = True
        await self.send_message("Seed rolling is now locked.")
        if self.state.get("use_french"):
            await self.send_message("Translate 'Seed rolling is now locked.' to French.")

    @monitor_cmd
    async def ex_unlock(self, args, message):
        self.state["locked"] = False
        await self.send_message("Seed rolling is now unlocked")
        if self.state.get("use_french"):
            await self.send_message("Translate 'Seed rolling is now locked' to French.")

    async def ex_rollseed(self, args, message):
        if self.state.get("locked"):
            await self.send_message("Seed rolling is locked! Only the creator of this room, a race monitor, or a moderator can roll a seed.")
            if self.state.get("use_french"):
                await self.send_message("Translate 'Seed rolling is locked! Only the creator of this room, a race monitor, or a moderator can roll a seed.'")
            return
            
        if self.state.get("permalink_available"):
            await self.send_message("The seed is already rolled! Use !permalink to view it.")
            if self.state.get("use_french"):
                await self.send_message("Translate 'The seed is already rolled! Use !permalink to view it.' to French.")

        await self.send_message("Rolling seed.....")
        generated_seed = self.generator.generate_seed(self.state.get("permalink"), self.state.get("generate_spoiler_log"))
        permalink = generated_seed.get("permalink")

        self.logger.info(permalink)

        self.state["permalink"] = permalink
        self.state["permalink_available"] = True

        await self.send_message(f"Permalink: {permalink}")
        await self.set_raceinfo(f" - {permalink}", False, False)
