import asyncio
from datetime import datetime, timedelta
from racetime_bot import RaceHandler, monitor_cmd, can_monitor
import random
import hashlib
import urllib.request
import string

from randobot.draft import Draft


class RandoHandler(RaceHandler):
    stop_at = ["cancelled", "finished"]

    STANDARD_RACE_PERMALINK = "IQwAACADspoBUgAAAAAAABCK2CA="
    STANDARD_SPOILER_RACE_PERMALINK = "IwUAAAAAwsXwJQAAAAAAgAAAAAA="

    def __init__(self, generator, **kwargs):
        super().__init__(**kwargs)

        self.generator = generator
        self.loop = asyncio.get_event_loop()
        self.loop_ended = False

    async def begin(self):
        if not self.state.get('intro_sent') and not self._race_in_progress():
            await self.send_message(
                "Welcome to Skyward Sword Randomizer! Setup your seed with !permalink <permalink> and !version <version> and roll with !rollseed"
            )
            await self.send_message(
                "If no permalink is specified, standard race settings will be used. "
                "If no version is specified, the version bundled with the bot will be used. Ask a member of the racing council for details on which version this is"
            )
            await self.send_message(
                "To enable draft mode, use !draft. Currently, draft mode must be self moderated, and is only designed for use in 1v1 races. If no picks or bans "
                "are specified, a random option will be selected from the list of possible options"
            )
            self.state['intro_sent'] = True
        self.state["permalink"] = self.STANDARD_RACE_PERMALINK
        self.state["spoiler"] = False
        self.state["version"] = None
        self.state["draft"] = None

    async def ex_francais(self, args, message):
        self.state["use_french"] = True
        await self.send_message("Bot responses will now also be in French.")
        await self.send_message("Translate 'Bot responses will now also be in French.' to French.")

    async def ex_log(self, args, message):
        if self.state.get("spoiler_url") and self.state.get("spoiler"):
            url = self.state.get("spoiler_url")
            await self.send_message(f"Spoiler Log can be found at {url}")

    async def ex_spoiler(self, args, message):
        spoiler = not self.state.get("spoiler")
        self.state["spoiler"] = spoiler
        if spoiler:
            await self.send_message("Will create a public sharable Spoiler Log")
        else:
            await self.send_message("Will NOT create a public sharable Spoiler Log")

    async def ex_info(self, args, message):
        response = ""
        if self.state.get("version") == None:
            response += "No version specified. Using bundled version. "
        else:
            response += f"Version: {self.state.get('version')} "
        response += f"Permalink: {self.state.get('permalink')} "
        if self.state.get("spoiler"):
            response += "Spoiler log will be generated and a link will be provided. "
        else:
            response += "Spoiler log will not be generated. "
        if self.state.get("peramlink_available"):
            response += "Seed has been rolled. Get it with !permalink. "
        else:
            response += "Seed not rolled. Roll with !rollseed. "
        await self.send_message(response)


    async def ex_seed(self, args, message):
        if not self.state.get("permalink_available"):
            await self.send_message("There is no seed! Please use !rollseed to get one")
            if self.state.get("use_french"):
                await self.send_message(
                    "Translate 'There is no permalink! Please use !rollseed to get a permalink' to French")
            return
        permalink = self.state.get("permalink")
        hash = self.state.get("hash")
        seed = self.state.get("seed")
        await self.send_message(f"Seed: {seed}, Hash: {hash}, Permalink: {permalink}")
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

    @monitor_cmd
    async def ex_reset(self, args, message):
        self.state["permalink"] = self.STANDARD_RACE_PERMALINK
        self.state["seed"] = None
        self.state["hash"] = None
        self.state["permalink_available"] = False
        self.state["spoiler"] = False
        self.state["spoiler_url"] = None
        self.state["version"] = None
        self.state["draft"] = None
        await self.send_message("The Seed has been reset.")

    async def ex_permalink(self, args, message):
        permalink = args[0]
        self.state["permalink"] = permalink
        await self.send_message(f"Updated permalink to {permalink}")

    async def ex_sgl(self, args, message):
        self.state["permalink"] = 'IQ0IIDsD85rpUwAAAAAAACHIFwA='
        await self.send_message(f"Updated the bot to SGL settings")

    async def ex_coop(self, args, message):
        self.state["permalink"] = 'oQ0AIBAD85oJUgAAAAAAAAAQAw=='
        self.state["version"] = '1.2.0_3868e57'
        await self.send_message("Updated the bot to Co-Op S1 settings")

    async def ex_version(self, args, message):
        version = args[0]
        self.state["version"] = version
        await self.send_message(f"Version set to {version}")

    async def ex_draft(self, args, message):
        if self.state["draft"] is not None:
            await self.send_message("Draft mode is already active")
        else:
            self.state["draft"] = Draft()
            await self.send_message("Draft mode activated. The !ban and !pick commands are now active")

    async def ex_draftoff(self, args, message):
        self.state["draft"] = None
        await self.send_message("Draft mode deactivated")

    async def ex_ban(self, args, message):
        if self.state["draft"] is None:
            await self.send_message("Draft mode is not active")
        else:
            if len(args) == 0:
                await self.send_message("No mode specified")
            else: 
                await self.send_message(self.state["draft"].ban(" ".join(args)))
    
    async def ex_pick(self, args, message):
        if self.state["draft"] is None:
            await self.send_message("Draft mode is not active")
        else:
            if len(args) == 0:
                await self.send_message("No mode specified")
            else: 
                await self.send_message(self.state["draft"].pick(" ".join(args)))
    
    async def ex_draftlog(self, args, message):
        if self.state["draft"] is None:
            await self.send_message("Draft mode is not active")
        else:
            if len(args) == 0:
                await self.send_message("Please specify 'off' or 'on' to deactivate or activate the randomizer's spoiler log generation.")
            else: 
                await self.send_message(self.state["draft"].set_log_state("".join(args).strip()))

    async def ex_draftstatus(self, args, message):
        draft = self.state["draft"]
        if draft is None:
            await self.send_message("Draft mode is not active")
        else:
            await self.send_message(f"Draft mode is active. Currently banned: {draft.banned}. Currently picked: {draft.picked}. Spoiler log: {draft.spoiler_log}.")
            
    async def ex_draftoptions(self, args, message):
        if self.state["draft"] is None:
            await self.send_message("Draft mode is not active")
        else:
            await self.send_message(f"Draft options: {', '.join(self.state['draft'].OPTIONS.keys())}")

    async def ex_rollseed(self, args, message):
        print("rolling seed")
        if self.state.get("locked") and not can_monitor(message):
            await self.send_message("Seed rolling is locked! Only the creator of this room, a race monitor, "
                                    "or a moderator can roll a seed.")
            if self.state.get("use_french"):
                await self.send_message("Translate 'Seed rolling is locked! Only the creator of this room, a race "
                                        "monitor, or a moderator can roll a seed.'")
            return

        if self.state.get("permalink_available"):
            await self.send_message("The seed is already rolled! Use !seed to view it.")
            if self.state.get("use_french"):
                await self.send_message("Translate 'The seed is already rolled! Use !permalink to view it.' to French.")
            return

        await self.send_message("Rolling seed.....")
        if self.state["draft"] is not None:
            (mode, perma) = self.state["draft"].make_selection()
            await self.send_message(f"Selected mode {mode}")
            self.state["permalink"] = perma
        if self.state.get("version") is None:
            generated_seed = self.generator.generate_seed(self.state.get("permalink"), self.state.get("spoiler"))
            permalink = generated_seed.get("permalink")
            hash = generated_seed.get("hash")
            seed = generated_seed.get("seed")
            version = generated_seed.get("version")
        else:
            version = self.state.get("version")
            commit = version.split('_')[1]
            seed_start = random.choice('123456789')
            seed_end = "".join(random.choice(string.digits) for _ in range(17))
            seed_name = seed_start + seed_end
            permalink = f"{self.state.get('permalink')}#{seed_name}"
            current_hash = hashlib.md5()
            current_hash.update(str(seed_name).encode("ASCII"))
            current_hash.update(permalink.encode("ASCII"))
            current_hash.update(version.encode("ASCII"))
            with urllib.request.urlopen(f"http://raw.githubusercontent.com/ssrando/ssrando/{commit}/names.txt") as f:
                data = f.read().decode("utf-8")
                names = [s.strip() for s in data.split("\n")]
            hash_random = random.Random()
            hash_random.seed(current_hash.digest())
            hash = " ".join(hash_random.choice(names) for _ in range(3))
            seed = seed_name    
            

        self.logger.info(permalink)

        self.state["permalink"] = permalink
        self.state["hash"] = hash
        self.state["seed"] = seed
        self.state["permalink_available"] = True

        await self.send_message(f"{version} Permalink: {permalink}, Hash: {hash}")

        if self.state.get("spoiler"):
            url = generated_seed.get("spoiler_log_url")
            self.state["spoiler_url"] = url
            await self.send_message(f"Spoiler Log URL available at {url}")
        
        if self.state["draft"] is not None:
            await self.set_raceinfo(f" - {version} Draft Option: {mode}, Seed: {seed}, Hash: {hash}, Permalink: {permalink}", False, False)
        else:
            await self.set_raceinfo(f" - {version} Seed: {seed}, Hash: {hash}, Permalink: {permalink}", False, False)

    def _race_in_progress(self):
        return self.data.get('status').get('value') in ('pending', 'in_progress')
