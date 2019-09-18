import time
import subprocess

boxes = ['192.168.0.151:5555',
         '192.168.0.152:5555',
         '192.168.0.153:5555',
         '192.168.0.154:5555',
         '192.168.0.155:5555',
         '192.168.0.156:5555',
         '192.168.0.157:5555',
         '192.168.0.158:5555',
         '192.168.0.159:5555',
         '192.168.0.160:5555',
         '192.168.0.161:5555',
         '192.168.0.162:5555',
         '192.168.0.163:5555',
         '192.168.0.164:5555',
         '192.168.0.165:5555',
         '192.168.0.166:5555',
         '192.168.0.167:5555',
         '192.168.0.168:5555',
         '192.168.0.169:5555',
         '192.168.0.170:5555',
         '192.168.0.171:5555',
         '192.168.0.172:5555',
         '192.168.0.173:5555',
         '192.168.0.174:5555',
         '192.168.0.175:5555',
         '192.168.0.176:5555',
         '192.168.0.177:5555',
         '192.168.0.178:5555',
         '192.168.0.179:5555',
         '192.168.0.180:5555',
         '192.168.0.181:5555',
         '192.168.0.182:5555',
         '192.168.0.183:5555',
         '192.168.0.184:5555',
         '192.168.0.185:5555',
         '192.168.0.186:5555',
         '192.168.0.187:5555',
         '192.168.0.188:5555',
         '192.168.0.189:5555',
         '192.168.0.190:5555',
         '192.168.0.191:5555',
         # '192.168.0.192:5555',
         # '192.168.0.193:5555',
         # '192.168.0.194:5555',
         # '192.168.0.195:5555',
         # '192.168.0.196:5555',
         ]

TVBOXES = {'TVBOX1':  '192.168.0.151:5555',
           'TVBOX2': '192.168.0.152:5555',
           'TVBOX3': '192.168.0.153:5555',
           'TVBOX4':  '192.168.0.154:5555',
           'TVBOX5': '192.168.0.155:5555',
           'TVBOX6': '192.168.0.156:5555',
           'TVBOX7':  '192.168.0.157:5555',
           'TVBOX8': '192.168.0.158:5555',
           'TVBOX9': '192.168.0.159:5555',
           'TVBOX10': '192.168.0.160:5555',
           'TVBOX11': '192.168.0.161:5555',
           'TVBOX12': '192.168.0.162:5555',
           'TVBOX13': '192.168.0.163:5555',
           'TVBOX14': '192.168.0.164:5555',
           'TVBOX15': '192.168.0.165:5555',
           'TVBOX16': '192.168.0.166:5555',
           'TVBOX17': '192.168.0.167:5555',
           'TVBOX18': '192.168.0.168:5555',
           'TVBOX19': '192.168.0.169:5555',
           'TVBOX20': '192.168.0.170:5555',
           'TVBOX21': '192.168.0.171:5555',
           'TVBOX22': '192.168.0.172:5555',
           'TVBOX23': '192.168.0.173:5555',
           'TVBOX24': '192.168.0.174:5555',
           'TVBOX25': '192.168.0.175:5555',
           'TVBOX26': '192.168.0.176:5555',
           'TVBOX27': '192.168.0.177:5555',
           'TVBOX28': '192.168.0.178:5555',
           'TVBOX29': '192.168.0.179:5555',
           'TVBOX30': '192.168.0.180:5555',
           'TVBOX31': '192.168.0.181:5555',
           'TVBOX32': '192.168.0.182:5555',
           'TVBOX33': '192.168.0.183:5555',
           'TVBOX34': '192.168.0.184:5555',
           'TVBOX35': '192.168.0.185:5555',
           'TVBOX36': '192.168.0.186:5555',
           'TVBOX37': '192.168.0.187:5555',
           'TVBOX38': '192.168.0.188:5555',
           'TVBOX39': '192.168.0.189:5555',
           'TVBOX40': '192.168.0.190:5555',
           'TVBOX41': '192.168.0.191:5555'
           }

LATEST = "0.153.1"


def reboot_all(running_procs):
    for id, device in enumerate(boxes):
        print("#### rebooting %s ####" % (device))
        running_procs.append(subprocess.Popen(["adb", "-s", device, "reboot"]))


def get_latest_pogo():
    cmd = "curl -L -o ./pogo.apk -k -s \"$(curl -k -s " \
          "'https://m.apkpure.com/pokemon-go/com.nianticlabs.pokemongo/download' | grep 'click here'|awk -F'\"' '{" \
          "print $12}')\""
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print("out: %s" % (output))


def update_pogo(running_procs):
    for device, serial in enumerate(boxes):
        if not is_outdated(serial):
            print("%s is up to date" % device)
            continue
        print("#### Updating %s ####" % (device))
        subprocess.call(["adb", "-s", serial, "shell", "am", "force-stop", "com.nianticlabs.pokemongo"])
        running_procs.append(
                subprocess.Popen(["adb", "-s", serial, "install", "-r", "/home/bree/repos/ADBKraken/pogo.apk"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT))


def update_pogodroid(running_procs):
    for device, serial in enumerate(boxes):
        print("#### Updating %s ####" % (device))
        running_procs.append(
                subprocess.Popen(["adb", "-s", serial, "install", "-r", "/home/bree/repos/ADBKraken/PogoDroid.apk"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT))


def connect():
    for device, serial in enumerate(boxes):
        print("#### Connecting %s ####" % (device))
        subprocess.call(["adb", "connect", serial])


def is_outdated(device):
    cmd = "adb -s %s shell dumpsys package com.nianticlabs.pokemongo | grep versionName" % device
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    version = ps.communicate()[0].decode("utf-8").strip().replace("versionName=", "")
    print("%s: %s" % (device, version))
    if version != LATEST:
        return True
    return False


def print_versions():
    for device, serial in enumerate(boxes):
        cmd = "adb -s %s shell dumpsys package com.nianticlabs.pokemongo | grep versionName" % serial
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        version = ps.communicate()[0].decode("utf-8").strip().replace("versionName=", "")
        print("%s: %s" % (device, version))
        if version != LATEST:
            print("%s: pogo version is outdated!" % (device))


if __name__ == '__main__':
    running_procs = []
    # connect()
    # update_pogodroid(running_procs)
    # get_latest_pogo()
    # print_versions()
    # update_pogo(running_procs)
    # reboot_all(running_procs)
    while running_procs:
        for proc in running_procs:
            retcode = proc.poll()
            if retcode is not None:  # Process finished.
                print(f"{proc.args} finshed")
                running_procs.remove(proc)
                break
            else:  # No process is done, wait a bit and check again.
                time.sleep(.1)
                continue
    print({f"TVBOX{x + 1}": y for x, y in enumerate(boxes)})
