# moderation

This repository contains moderation tools and data for [thegem.city](https://thegem.city/).

# Usage

1. Generate a token via your application settings page: https://thegem.city/settings/applications
2. Run the python script `python ./update_blocklist.py --token=[TOKEN]`

Alternatively, you can set the environment variable `TOKEN` instead of the `--token` argument.

## Full Setup (Ubuntu)

1. Install python, pip, and venv: `apt-get install python3-venv`
2. Create a local venv: `python3 -m venv ./venv`
3. Install dependencies: `./venv/bin/pip install aiohttp`
