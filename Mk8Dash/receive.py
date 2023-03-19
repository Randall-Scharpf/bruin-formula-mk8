from PyQt5.QtCore import QRunnable, Qt, QThreadPool, pyqtSignal
from can import Message
import os
import can
import time

# https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
# https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-2-autostart

PROCESS_FAKE_MSG = True
fake_msg_num = 0
PRINT_MSG = True

# analog update time to 20, improve efficiency

if not PROCESS_FAKE_MSG:
    os.system('sudo ip link set can0 type can bitrate 500000')
    os.system('sudo ifconfig can0 up')
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

# https://www.aemelectronics.com/sites/default/files/aem_product_instructions/Infinity-ECU-Full-Manual.pdf
# https://www.pragmaticlinux.com/2021/10/can-communication-on-the-raspberry-pi-with-socketcan/
# https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf
# https://forums.raspberrypi.com/viewtopic.php?t=141052
# https://harrisonsand.com/posts/can-on-the-raspberry-pi/

TIMEOUT = 10
MSGID_1 = 0x01F0A000
MSGID_2 = 0x01F0A003
MAX_BLUR_THROTTLE = 50  # percent throttle at which blur reaches max effect


class Receive(QRunnable):
    def __init__(self, update_gui, update_timestamp):
        super().__init__()
        self.keep_running = True
        self.update_gui = update_gui
        self.update_timestamp = update_timestamp

    def run(self):
        while self.keep_running:
            if PROCESS_FAKE_MSG:
                time.sleep(0.001)
                msg = test_msgid2()
            else:
                msg = can0.recv(TIMEOUT)
            if PRINT_MSG:
                print("Recv:", msg)
            if msg is None:
                print('Timeout: occurred, no message.')
            else:
                self.parse_message(msg.arbitration_id, msg.data, msg.timestamp)

    def stop(self):
        self.keep_running = False
        if not PROCESS_FAKE_MSG:
            os.system('sudo ifconfig can0 down')

    def parse_message(self, id, data, timestamp):
        if id == MSGID_1:
            data_dict = {}
            # byte 0-1, Engine Speed, 16 bit unsigned, scaling 0.39063 rpm/bit, range 0 to 25,599.94 RPM
            data_dict['rpm'] = (data[0] * 256 + data[1]) * 0.39063 / 1000
            # byte 4-5, Throttle, 16 bit unsigned, scaling 0.0015259 %/bit, range 0 to 99.998 %
            throttle = (data[4] * 256 + data[5]) * 0.0015259
            data_dict['blur'] = min(1, max(0, throttle / MAX_BLUR_THROTTLE))
            # byte 7, Coolant Temp,  8 bit signed 2's comp, scaling 1 Deg C/bit 0, range -128 to 127 C
            data_dict['coolant'] = data[7] if data[7] >= 128 else data[7] - 128
            if PRINT_MSG:
                print("MSGID_1: rpm", data_dict['rpm'], "throttle", throttle, "coolant", data_dict['coolant'])
            self.update_gui.emit(data_dict)
        elif id == MSGID_2:
            data_dict = {}
            # byte 0, Lambda #1, 8 bit unsigned, scaling 0.00390625 Lambda/bit, offset 0.5, range 0.5 to 1.496 Lambda
            data_dict['lambda'] = data[0] * 0.00390625 + 0.5
            # byte 2-3, Vehicle Speed, 16 bit unsigned, scaling 0.0062865 kph/bit, range 0 to 411.986 km/h
            data_dict['speed'] = (data[2] * 256 + data[3]) * 0.0062865
            # 6-7 Battery Volts 16 bit unsigned 0.0002455 V/bit 0 to 16.089 Volts
            data_dict['battery'] = (data[6] * 256 + data[7]) * 0.0002455
            if PRINT_MSG:
                print("MSGID_2: lambda1", data_dict['lambda'], "speed", data_dict['speed'], "battery", data_dict['battery'])
            self.update_gui.emit(data_dict)
        else:
            if PRINT_MSG:
                print("MSGID_UNK, skipped")
        self.update_timestamp.emit(timestamp)


def test_msgid1():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    return Message(data=bytearray([int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0, 0, int(fake_msg_num)]), arbitration_id=MSGID_1)


def test_msgid2():
    global fake_msg_num
    fake_msg_num = min(fake_msg_num + 0.1, 255)
    return Message(data=bytearray([int(fake_msg_num), 0, int(fake_msg_num), 0, 0, 0, int(fake_msg_num), 0]), arbitration_id=MSGID_2)


def test_timer():
    global fake_msg_num
    fake_msg_num += 0.005
    if int(fake_msg_num) % 2 == 0:
        return None
    return Message(data=bytearray([]), arbitration_id=0, timestamp = fake_msg_num * 10)
