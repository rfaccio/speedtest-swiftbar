#! /usr/bin/python3

# <xbar.title>Speedtest</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Rafael Faccio</xbar.author>
# <xbar.author.github>rfaccio</xbar.author.github>
# <xbar.desc>Displays latest network speed test using speedtest-cli</xbar.desc>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>

from datetime import datetime
import subprocess
import json

def runSpeedtest():
    speedtestResponse = subprocess.run(
        ['/opt/homebrew/bin/speedtest', '--json', '--share'], capture_output=True, text=True).stdout
    return processPayload(speedtestResponse)


def processPayload(payload):
    speedtestJson = json.loads(payload)

    stringDownload = str(round(float(speedtestJson['download']/1e+6)))
    stringUpload = str(round(float(speedtestJson['upload']/1e+6)))
    ping = speedtestJson['ping']
    serverName = speedtestJson['server']['name']
    serverCountry = speedtestJson['server']['cc']
    serverSponsor = speedtestJson['server']['sponsor']
    shareUrl = speedtestJson['share']

    testTime = datetime.now().strftime("%H:%M:%S")

    results = (stringDownload, stringUpload, ping, serverSponsor,
            serverName, serverCountry, testTime, shareUrl)

    return results


def printResults(results):
    header = (
        '{0} :icloud.and.arrow.down: {1} :icloud.and.arrow.up:').format(*results)

    body = ('Ping: {2} ms' +
            '\nServer: {3} - {4}/{5}' +
            '\nLast Test: {6}'
            ).format(*results)

    options = ('Share Result | href={7}' +
                     '\nRefresh | refresh=True').format(*results)

    print(header)
    print('\n---\n')
    print(body)
    print('\n---\n')
    print(options)


try:
    printResults(runSpeedtest())
except FileNotFoundError as error:
    print('speedtest-cli is missing')
except:
    pass