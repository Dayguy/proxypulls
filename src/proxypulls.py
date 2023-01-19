#!/usr/bin/env python

import os
import io
import json
import shutil
import requests
import argparse

PROXYCHAINS_CONF = "/etc/proxychains.conf"

def backup():
    try:
        if PROXYCHAINS_CONF:
            backupName = PROXYCHAINS_CONF + ".orig"
            shutil.copy2(PROXYCHAINS_CONF, backupName)
        else: 
            print("Trouble copying {}".format(PROXYCHAINS_CONF))
    except:
        print("Unable to locate {}".format(PROXYCHAINS_CONF))

def setConf(proxyList):
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
        if jData['isAlive']:
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

    backup()
    setConf(proxies)

if __name__ == "__main__":
    main()