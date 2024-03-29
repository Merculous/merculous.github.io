import asyncio

from pyodide.ffi import JsException
from pyodide.http import pyfetch

async def getJSONData(url):
    try:
        r = await pyfetch(
            url=url,
            method='GET'
        )
    except JsException as e:
        print(f'Got JsException: {e}')
    else:
        if r.ok:
            data = await r.json()
            return data

class API:
    def __init__(self, device: str = None):
        self.home = 'https://api.ipsw.me/v4'
        self.device = device

    async def getAllDevices(self):
        url = f'{self.home}/devices'
        data = await getJSONData(url)
        return data

    async def getDeviceInfo(self):
        if self.device:
            url = f'{self.home}/device/{self.device}'
            data = await getJSONData(url)
            return data
        else:
            raise Exception('No device was passed!')

    async def getSignedVersionsForDevice(self):
        data = await self.getDeviceInfo()
        versions = data.get('firmwares')
        signed = {}

        for version in versions:
            if version.get('signed'):
                signed[version.get('version')] = []
                if version.get('buildid') not in signed[version.get('version')]:
                    signed[version.get('version')].append(version.get('buildid'))

        return signed

    async def getAllSignedVersions(self):
        devices = await self.getAllDevices()
        signed = {}

        for device in devices:
            self.device = device.get('identifier')
            signed_versions = await self.getSignedVersionsForDevice()
            signed[self.device] = {}
            signed[self.device].update(signed_versions)
        
        return signed
