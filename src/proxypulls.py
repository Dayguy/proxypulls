#!/usr/bin/env python

import os
import io
import json
import requests
import argparse

PROXYCHAINS_CONF = "/etc/proxychains.conf"

# def backup(file):
#     backupName = file + ".orig"
#     print(backupName)
#     shutil(file, backupName)

def setConf(proxyList):
    # backup(PROXYCHAINS_CONF)
    newLines = []
    with io.open(PROXYCHAINS_CONF, 'r') as orig:
        for line in orig.readlines():
            newLines.append(line)
            if line.strip() == "[ProxyList]":
                break

    orig.close()

    # Append our new proxy entries to the new config
    # newLines.extend(proxyList)
    for proxy in proxyList:
        newLines.append(proxy)

    # Write the config back out
    with io.open(PROXYCHAINS_CONF, 'w') as new:
        new.writelines(newLines)

    new.close()


def getProxy():
    baseUrl = "https://public.freeproxyapi.com"
    endPoint = "/api/Proxy/Medium"
    myResponse = requests.get("{}{}".format(baseUrl, endPoint))
    if (myResponse.ok):
        jData = json.loads(myResponse.content)
        return jData['type'].lower() + " " + jData['host'] + " " + str(jData['port'])


def main():
    proxies = []
    defaultCount = 1
    proxyCount = 1

    parser = argparse.ArgumentParser(description='Set a new list of proxy for use with ProxyChains.')
    parser.add_argument(
        '--total',
        type=int,
        default=defaultCount,
        dest='proxyCount',
        help='How many proxy to add'
    )
    args = parser.parse_args()

    # Retrieve the desired number of proxies
    for x in range(args.proxyCount):
        proxy = getProxy()
        proxies.append(proxy + '{}'.format(os.linesep))

    setConf(proxies)


if __name__ == "__main__":
    main()