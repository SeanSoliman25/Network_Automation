#!/usr/bin/python
#
# Copyright (c) 2018  Krishna Kotha <krkotha@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# This script retrieves entire interface configuration from a network element via RESTCONF

# import the requests library
import requests
import sys
import json

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

# use your user credentials to access the Cat9300
cred_list = [
    {"user":"sakmsoliman", "password":"WoJAY29xb_-b5"}
    ]

# url string to issue GET request
url = "devnetsandboxiosxec8k.cisco.com"
url = f"https://{url}/restconf/data/Cisco-IOS-XE-native:native"

# create a main() method
def main():
    try:
        for cred in cred_list:
            """Main method that retrieves the Interface details from Cat9300 via RESTCONF."""

            # RESTCONF media types for REST API headers
            headers = {'Content-Type': 'application/yang-data+json',
                       'Accept': 'application/yang-data+json'}
            # this statement performs a GET on the specified url
            response = requests.get(url, auth=(cred["user"], cred["password"]),
                                    headers=headers, verify=False)

            print(f"HTTP Status Code: {response.status_code}\n")

            response.raise_for_status()

            resp_dict = response.json()["Cisco-IOS-XE-native:native"]["interface"]

            # print(json.dumps(response.json(), indent=2))

            # print the json that is returned
            for interface in resp_dict:
                for port in resp_dict[interface]:
                    print(f"{interface} {port['name']}")
                    if "description" in port:
                        print(f"\tDescription: {port['description']}")
                    try:
                        port_ip = port["ip"]
                        port_main = port_ip["address"]["primary"]
                        print(f"\tIP Address: {port_main['address']}")
                        print(f"\tIP Mask: {port_main['mask']}")
                        if "helper-address" in port_ip:
                            for port_helper in port_ip['helper-address']:
                                print(f"\tHelper Address: {port_helper['address']}")
                    except:
                        print("\tNo IP Configuration")
                    if "shutdown" in port:
                        print("\tPort Manually Shutdown")
                    else:
                        print("\tPort Is Enabled")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the router.")
    except requests.exceptions.Timeout:
        print("Connection timed out.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP request failed: {e}")
    except (ValueError, KeyError) as e:
        print(f"Could not parse interface response: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    sys.exit(main())