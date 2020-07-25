#!/usr/bin/env python

import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import operator


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--controller", default="localhost", help='the controller address (default "localhost")',
)
parser.add_argument(
    "-u", "--username", default="admin", help='the controller username (default("admin")',
)
parser.add_argument("-p", "--password", default="", help="the controller password")
parser.add_argument(
    "-b", "--port", type=int, default=8443, help='the controller port (default "8443")',
)
parser.add_argument(
    "-s", "--step", type=int, default=4, help="only reset every x units (default 4)",
)
parser.add_argument(
    "-m", "--modulus", type=int, default=0, help="reset units starting with number (default 0)",
)
parser.add_argument(
    "-t", "--type", default="uap", help='the type of device to reset (default "uap")',
)
parser.add_argument(
    "-v", "--verify", type=str2bool, default=False, help="verify SSL requests",
)
parser.set_defaults(verify=False)
args = parser.parse_args()

if not args.verify:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

base_url = "https://" + args.controller + ":" + args.port
login_url = base_url + "/api/login"
login_data = {"username": args.username, "password": args.password}
default_headers = {"Origin": base_url}

login_cookies = requests.post(login_url, json=login_data, headers=default_headers, verify=args.verify).cookies

sites = requests.get(
    base_url + "/api/self/sites", cookies=login_cookies, headers=default_headers, verify=args.verify,
).json()

for site in sites["data"]:
    site_name = site["name"]
    device_list = sorted(
        requests.get(
            base_url + "/api/s/" + site_name + "/stat/device",
            cookies=login_cookies,
            headers=default_headers,
            verify=args.verify,
        ).json()["data"],
        key=lambda device: device["name"],
    )
    for device_index, device in enumerate(device_list):
        if device["type"] == args.type and device_index % args.step == args.modulus:
            requests.post(
                base_url + "/api/s/" + site_name + "/cmd/devmgr",
                cookies=login_cookies,
                headers=default_headers,
                json={"mac": device["mac"], "reboot_type": "soft", "cmd": "restart",},
                verify=args.verify,
            )
