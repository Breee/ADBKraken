import subprocess
import config as config

from utility.globals import LOGGER
from utils import sorted_nicely

class ADBmanager(object):

    def __init__(self):
        self.devices = config.DEVICES

    def __connect(self, device, serial):
        LOGGER.info("#### Connecting to %s ####" % (device))
        ps = subprocess.Popen(["adb", "connect", serial], stdout=subprocess.PIPE)
        output = ps.communicate()[0].decode('utf-8')
        return output

    def connect_all(self):
        outputs = []
        for device, serial in self.devices.items():
            output = self.__connect(device, serial)
            if 'connected' in output:
                output = 'connected'
            else:
                output = 'unreachable'
            outputs.append("%s : %s : %s" % (device, serial, output))
        return "\n".join(sorted_nicely(outputs))

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

    def __reboot_all(self):
        outputs = []
        for device, serial in self.devices.items():
            output = self.__reboot(device, serial)
            outputs.append("%s : %s : %s" % (device, serial, output))
        return "\n".join(sorted_nicely(outputs))

    def reboot(self, device=None):
        if device is not None and device in self.devices:
            self.__reboot(device, serial=self.devices[device])
        elif device is None:
            self.__reboot_all()
