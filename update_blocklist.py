from typing import Set
import os
import asyncio
import argparse
import aiohttp


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default=os.environ.get("SERVER", "thegem.city"))
    parser.add_argument("--token", default=os.environ.get("TOKEN"))
    parser.add_argument("--source", default=os.environ.get("SOURCE", "./domains"))
    parser.add_argument("--severity", default=os.environ.get("SEVERITY", "suspend"))

    args = parser.parse_args()

    if not args.server or not args.token or not args.source:
        exit(parser.print_usage())

    domains: Set[str] = await get_domains(args.source)

    url = f"https://{args.server}/api/v1/admin/domain_blocks"

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {args.token}"}

        blocked_domains: Set[str] = await get_current_blocks(session, headers, url)

        # print(f"currently blocked domains: {blocked_domains}")
        for domain in domains:
            if domain in blocked_domains:
                continue
            async with session.post(
                url, headers=headers, data={"domain": domain, "severity": args.severity}
            ) as resp:
                print(f"{domain} {resp.status}")


async def get_current_blocks(session, headers, url) -> Set[str]:
    url_queue: Set[str] = set([url])
    checked_urls: Set[str] = set()
    results: Set[str] = set()

    while url is not None:
        async with session.get(url, headers=headers) as resp:
            url = None

            if resp.status != 200:
                exit("unable to retrieved blocked domains")

            links = [value.strip() for value in resp.headers.get("Link", "").split(",")]
            for link in links:
                if '; rel="next"' in link:
                    url = link.replace('; rel="next"', "").strip("<>")

            for blocked_domain in await resp.json():
                results.add(blocked_domain.get("domain"))
    return results


async def get_domains(domain_blocks_source: str) -> Set[str]:
    if domain_blocks_source.startswith("http://"):
        exit("source must either be a local file or an HTTPS url")
    if domain_blocks_source.startswith("https://"):
        async with aiohttp.ClientSession() as session:
            async with session.get(domain_blocks_source) as resp:
                if resp.status != 200:
                    exit("unable to retrieved blocked domains list")
                resp_text = await resp.text()
                return set(resp_text.split("\n"))
    with open("./domains", mode="r", encoding="utf-8") as fd:
        return set(fd.read().split("\n"))


if __name__ == "__main__":
    asyncio.run(main())
