import subprocess
import asyncio
import time
import config as config

from utility.globals import LOGGER
from utils import sorted_nicely

class ADBmanager(object):

    def __init__(self):
        self.devices = config.DEVICES
        self.running_processes = []

    async def run(self,cmd):
        proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        return stdout.decode('utf-8'), stderr.decode('utf-8')

    async def connect_all(self):
        results = await asyncio.gather(*[self.run(f"adb connect {serial}") for device, serial in self.devices.items()])
        output = []
        for id, out in enumerate(results, start=0):
            output.append((list(self.devices.items())[id][0], list(self.devices.items())[id][1], out[0], out[1]))
        return output

    def get_devices(self):
        ps = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE)
        output = ps.communicate()[0].decode('utf-8')
        return output

    def get_pogo_versions(self):
        versions = []
        for device, serial in self.devices.items():
            cmd = "adb -s %s shell dumpsys package com.nianticlabs.pokemongo | grep versionName" % serial
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            version = ps.communicate()[0].decode("utf-8").strip().replace("versionName=", "")
            if version != "0.149.1":
                version += "(outdated)"
            versions.append("%s: %s : %s" % (device, serial, version))
        return "\n".join(sorted_nicely(versions))

    def __reboot(self, device, serial):
        LOGGER.info("#### Rebooting %s ####" % (device))
        ps = subprocess.Popen(["adb", "-s", serial, "reboot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = ps.communicate()[0].decode('utf-8')
        return output

    def __reboot_list(self, device_names):
        LOGGER.info("#### Got list to reboot %s ####" % (str(device_names)))
        outputs = []
        devices = [(device_name, self.devices[device_name]) for device_name in device_names]
        for device, serial in devices:
            output = self.__reboot(device, serial)
            outputs.append("%s : %s : %s" % (device, serial, output))
        return outputs

    def __reboot_all(self):
        outputs = []
        for device, serial in self.devices.items():
            output = self.__reboot(device, serial)
            outputs.append("%s : %s : %s" % (device, serial, output))
        return "\n".join(sorted_nicely(outputs))

    def reboot(self, device_names=None):
        output = "return: "
        print(device_names)
        if device_names is not None and device_names:
            output += str(self.__reboot_list(device_names))
        elif device_names is None or not device_names:
            output += str(self.__reboot_all())
        return output
