from datetime import datetime
from github import Github, InputFileContent
import os
import random
import string
import re
import time


class Generator:
    def __init__(self, github_token):
        self.github_token = github_token

    def generate_seed(self, permalink, spoiler):
        seed_start = "".join(random.choice('123456789') for _ in range(1))
        seed_end = "".join(random.choice(string.digits) for _ in range(17))
        seed_name = seed_start + seed_end
        file_name = "".join(random.choice(string.digits) for _ in range(18))

        os.system(f"python sslib/randoscript.py --dry-run --noui --seed={seed_name} --permalink={permalink}")
        os.wait()
        try:
            spoiler_log_file_name = f"SS Random {seed_name} - Spoiler Log.txt"
            spoiler_log_file = open(spoiler_log_file_name, "r")

        except FileNotFoundError:
            spoiler_log_file_name = f"SS Random {seed_name} - Anti Spoiler Log.txt"
            spoiler_log_file = open(spoiler_log_file_name, "r")

        bare_log = spoiler_log_file.read()
        log = bare_log.split('\n')

        version = log[0]
        permalink = log[1].split(' ')[1]
        hash_re = re.compile('Hash : (.*)')
        rando_hash = hash_re.findall(log[3])[0]

        spoiler_log_file.close()

        if spoiler:

            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            gh = Github(self.github_token)
            gh_auth_user = gh.get_user()
            gist = gh_auth_user.create_gist(
                public=False,
                files={f"spoiler_log_{timestamp}.txt": InputFileContent(bare_log)},
                description="Skyward Sword Randomizer Spoiler Log"
            )
            spoiler_log_url = gist.html_url

            return {
                "permalink": permalink,
                "file_name": file_name,
                "seed": seed_name,
                "hash": rando_hash,
                "spoiler_log_url": spoiler_log_url,
                "version": version
            }

        else:
            return {
                "permalink": permalink,
                "file_name": file_name,
                "seed": seed_name,
                "hash": rando_hash,
                "version": version
            }
