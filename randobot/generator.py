from datetime import datetime
from github import Github, InputFileContent
import os
import random
import string
import uuid


class Generator:
    def __init__(self, github_token):
        self.github_token = github_token

    def generate_seed(self, permalink, generate_spoiler_log):
        seed_name = uuid.uuid4()
        file_name = "".join(random.choice(string.digits) for _ in range(6))

        os.system(f"python sslib/ssrando.py -seed={seed_name} -permalink={permalink}")

        permalink_file_name = f"permalink_{seed_name}.txt"
        permalink_file = open(permalink_file_name, "r")
        permalink = permalink_file.read()
        permalink_file.close()

        if generate_spoiler_log:
            spoiler_log_file_name = f"SS Random {seed_name} - Spoiler Log.txt"
            spoiler_log_file = open(spoiler_log_file_name, "r")
            spoiler_log = spoiler_log_file.read()
            spoiler_log_file.close()

            timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            gh = Github(self.github_token)
            gh_auth_user = gh.get_user()
            gist = gh_auth_user.create_gist(
                public=False,
                files={f"spoiler_log_{timestamp}.txt": InputFileContent(spoiler_log)},
                description="Skyward Sword Randomizer Spoiler Log"
            )
            spoiler_log_url = gist.html_url
        else:
            spoiler_log_url = None

        return {
            "permalink": permalink,
            "file_name": file_name,
            "spoiler_log_url": spoiler_log_url
        }