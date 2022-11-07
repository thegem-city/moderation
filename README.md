# moderation

This repository contains moderation tools and data for [thegem.city](https://thegem.city/).

# Internals

This uses the `/api/v1/admin/domain_blocks` API resource to retrieve the list of currently blocked domains at the server level and then block any domains from a given domain source.

The source can either be an HTTPS resource or a local file.

# Usage

1. Generate a token via your application settings page: https://thegem.city/settings/applications
2. Run the python script `python ./update_blocklist.py --token=[TOKEN]`

Alternatively, you can set the environment variable `TOKEN` instead of the `--token` argument.

## Full Setup (Ubuntu)

1. Install python, pip, and venv: `apt-get install python3-venv`
2. Create a local venv: `python3 -m venv ./venv`
3. Install dependencies: `./venv/bin/pip install aiohttp`

# GitHub Workflow

You can easily adapt this to your own instance with a few small changes:

1. Create a GitHub environment called "production" and set the "MASTO_TOKEN" secret to the generated token in the `Usage` step.
2. Update the python script executable step to include your server URL and source:

```yaml
- run: python ./update_blocklist.py
  env:
    TOKEN: ${{ secrets.MASTO_TOKEN }}
    SERVER: your-instance.com
    SOURCE: "./domains"
    SEVERITY: "suspend"
```

Bonus points if you have steps for multiple files for different severities.
