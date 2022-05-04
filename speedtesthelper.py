from cProfile import run
from datetime import datetime
import subprocess
import json


def runSpeedtest():
    speedtestResponse = subprocess.run(
        ['/opt/homebrew/bin/speedtest', '--json', '--share'], capture_output=True, text=True).stdout
    header, body, options = processPayload(speedtestResponse)
    return header, body, options


def processPayload(payload):
    speedtestJson = json.loads(payload)

    ping = speedtestJson['ping']
    download = speedtestJson['download']/1e+6
    upload = speedtestJson['upload']/1e+6
    serverName = speedtestJson['server']['name']
    serverCountry = speedtestJson['server']['cc']
    serverSponsor = speedtestJson['server']['sponsor']
    shareUrl = speedtestJson['share']

    testTime = datetime.now().strftime("%H:%M:%S")

    stringDownload = str(round(float(download)))
    stringUpload = str(round(float(upload)))

    args = (stringDownload, stringUpload, ping, serverSponsor,
            serverName, serverCountry, testTime, shareUrl)

    header = (
        '{0} :icloud.and.arrow.down: {1} :icloud.and.arrow.up:').format(*args)

    body = ('Ping: {2}' +
            '\nServer: {3} - {4}/{5}' +
            '\nLast Test: {6}'
            ).format(*args)

    optionsOutput = ('Share Result | href={7}' +
                     '\nRefresh | refresh=True').format(*args)

    return header, body, optionsOutput


def printResults(header, body, options):
    print(header)
    print('\n---\n')
    print(body)
    print('\n---\n')
    print(options)


header, body, options = runSpeedtest()
printResults(header, body, options)
