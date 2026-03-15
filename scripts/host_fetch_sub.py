#!/usr/bin/env python3
"""Fetch a subscription on the host and hand it to a local subconverter.

This is useful when the host can reach a subscription URL, but the Docker
container running subconverter cannot resolve or fetch it directly.
"""

import argparse
import base64
import sys
import urllib.parse
import urllib.request
from typing import Optional


def read_subscription_url(arg_url: Optional[str]) -> str:
    if arg_url:
        return arg_url.strip()

    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return data

    raise SystemExit(
        "missing subscription URL: pass it as an argument or pipe it on stdin"
    )


def fetch_subscription(url: str, user_agent: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def build_subconverter_url(
    backend: str, target: str, subscription_bytes: bytes, config: Optional[str]
) -> str:
    data_url = "data:text/plain;base64," + base64.b64encode(subscription_bytes).decode()
    query = {
        "target": target,
        "url": data_url,
    }
    if config:
        query["config"] = config
    return backend.rstrip("/") + "/sub?" + urllib.parse.urlencode(query)


def fetch_converted_output(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a subscription on the host and convert it through a local "
            "subconverter instance."
        )
    )
    parser.add_argument(
        "subscription_url",
        nargs="?",
        help="remote subscription URL; omit to read from stdin",
    )
    parser.add_argument(
        "--backend",
        default="http://127.0.0.1:25500",
        help="local subconverter base URL (default: %(default)s)",
    )
    parser.add_argument(
        "--target",
        default="clash",
        help="subconverter target format (default: %(default)s)",
    )
    parser.add_argument(
        "--config",
        help="optional external config URL/path to pass through to subconverter",
    )
    parser.add_argument(
        "--user-agent",
        default="Clash",
        help="User-Agent used when fetching the source subscription",
    )
    parser.add_argument(
        "--fetch-output",
        action="store_true",
        help="fetch the converted content immediately instead of printing the URL",
    )
    parser.add_argument(
        "--output",
        help="write converted output to a file; implies --fetch-output",
    )
    args = parser.parse_args()

    subscription_url = read_subscription_url(args.subscription_url)
    subscription_bytes = fetch_subscription(subscription_url, args.user_agent)
    subconverter_url = build_subconverter_url(
        args.backend, args.target, subscription_bytes, args.config
    )

    if not args.fetch_output and not args.output:
        print(subconverter_url)
        return 0

    converted_output = fetch_converted_output(subconverter_url)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(converted_output)
    else:
        print(converted_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
