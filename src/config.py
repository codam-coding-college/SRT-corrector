# SUBTITLE-CORRECTOR IS LICENSED UNDER THE GNU GPLv3
# Copyright (C) 2023 Will Maguire

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# The definition of Free Software is as follows:
# 	- The freedom to run the program, for any purpose.
# 	- The freedom to study how the program works, and adapt it to your needs.
# 	- The freedom to redistribute copies so you can help your neighbor.
# 	- The freedom to improve the program, and release your improvements
#   - to the public, so that the whole community benefits.

# A program is free software if users have all of these freedoms.

import platform
import json
import os

# Default recommended config. 
# Model should be the most up to date and cheapest GPT4 model.
# Prompt directory will be generated by the generate_default_config() function differently depending on the OS used.
# The sweet spot for tokens per query is from 150-300, results above or below that may vary.
default_config = {
    "model": "gpt-4-turbo",
    "tokens_per_query": 300,
    "prompt_directory": "",
    "tier": 1
}

# Rudimentary config class.
class Config():
    def __init__(self, prompt=""): 
        config_path, config_dir = self.determine_config_path() 
        if (not os.path.exists(config_path)):
            self.generate_default_config(config_path, config_dir)
        with open(config_path) as f:     
            obj = json.loads(f.read()) # Open & read config file.
        # "Tier" of the organisation, see https://platform.openai.com/docs/guides/rate-limits/usage-tiers
        self.tier = obj['tier']
        self.model = obj['model'] # Model to use.
        self.prompt_directory = obj['prompt_directory'] # Directory where prompts are stored.
        self.tokens_per_query = obj['tokens_per_query'] # Amount of tokens per query.
        self.prompt = prompt # Prompt to use.

    # If a config is not found, this function will be called and prompt the user to generate and install one.     
    def generate_default_config(self, config_path, config_dir):
        print("No config file found. Do you want to generate and install a default config?")
        result = self.question(f"Config file will be stored in: {config_path}. Proceed? (y/n) ")
        if result is True:
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            with open(config_path, "w") as f:
                default_config["prompt_directory"] = os.path.join(os.path.expanduser("~"), "prompts").replace("\\", "\\\\")
                print(f"Your prompt directory will be located here: {default_config['prompt_directory']}")
                f.write(json.dumps(default_config))
        elif result is False:
            print("Cannot continue without config. Program exiting.")
            exit()
            
    # Quick helper function to determine what path the user's config should be stored at.
    def determine_config_path(self):
        name = "subtitle-corrector"
        home = os.path.expanduser("~")
        if (platform.system() == "Linux"):
            config_dir = os.path.join(home, ".config", name)
            config_path = os.path.join(home, ".config", name, "config.json")
        elif (platform.system() == "Darwin"):
            config_dir = os.path.join(home, "Library", "Application Support", name) 
            config_path = os.path.join(home, "Library", "Application Support", name, "config.json") 
        elif (platform.system() == "Windows"):
            config_dir = os.path.join(home, "AppData", "Local", name)
            config_path = os.path.join(home, "AppData", "Local", name, "config.json")
        else:
            print("Unsupported OS, exiting.")
            exit()
        return (config_path, config_dir)
    
    # Helper function to get a user's consent. 
    def question(self, message):
        while True:
            result = input(message)
            if result in ['y', 'yes']:
                return (True)
            elif result in ['n', 'no']:
                return (False)
