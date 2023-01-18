import requests
import json
import sys

def getProxy():
    baseUrl = "https://public.freeproxyapi.com"
    endPoint = "/api/Proxy/Medium"
    myResponse = requests.get("{}{}".format(baseUrl, endPoint))
    if (myResponse.ok):
        jData = json.loads(myResponse.content)
        return jData['type'] + " " + jData['host'] + " " + str(jData['port'])
    else:
        myResponse.raise_for_status()

def main():
    args = sys.argv[1:]
    proxyBlock = ""
    if (len(args) == 2 and args[0] == "-n"):
        proxyCount = int(args[1])

    for x in range(proxyCount):
        proxyBlock += getProxy() + "\n"

    print(proxyBlock)


if __name__ == "__main__":
    main()