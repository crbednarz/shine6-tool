from enum import Enum
from struct import unpack_from, unpack, pack_into, pack


class LightingMode(Enum):
    Solid = 0
    Rainbow = 1
    Breathing = 2
    Reactive = 3
    Wave = 4
    Custom = 0xB0


class FlashMode(Enum):
    Firmware = 0x04
    Version = 0x00


class BootMode(Enum):
    Flashing = 0x00
    Normal = 0x01

class Packet:
    def __init__(self, data, delay=0.01):
        self.data = bytearray(64)
        self.data[0:len(data)] = data
        self.delay = delay

def lock_settings():
    return [
        Packet([0x41, 0x1])
    ]


def unlock_settings():
    return [
        Packet([0x41, 0x0])
    ]


def use_host_lighting():
    return [
        Packet([0x51, 0x30])
    ]


def use_lighting_mode(mode):
    if not isinstance(mode, LightingMode):
        raise ValueError("\"mode\" must be of type LightingMode")
    return [
        Packet(pack("<II", 0x2851, mode.value))
    ]


def query_string(id):
    return [
        Packet([0x12, id])
    ]


def set_flash_mode(mode):
    # Honestly not too sure what this address command is actually doing.
    # It seems to be important to settings up the flashing process.
    if mode == FlashMode.Firmware:
        address_command = Packet([0x1d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xd0], delay=0.1)
    elif mode == FlashMode.Version:
        address_command = Packet([0x1d, 0x01, 0x04, 0x28, 0x70], delay=0.1)
    else:
        raise ValueError("\"mode\" is not a recognized value of type FlashMode")

    return [
        address_command,
        Packet([0x1e, 0x01, 0x00, 0x00, 0x00, mode.value], delay=0.1),
        Packet([0x1e, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff], delay=0.1)
    ]


def boot_into(mode):
    if not isinstance(mode, BootMode):
        raise ValueError("\"mode\" must be of type BootMode")
    return [
        Packet([0x11, mode.value])
    ]


def finalize_flashing():
    # Really not sure what this command does, but it appears to happen
    # after flashing completes and the device is booted into normal usage.
    return [
        Packet([0x10, 0x02], delay=0.1)
    ]


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def flash_data(data):
    return [
        Packet([0x1f, len(chunk), 0x00, 0x00] + list(chunk))
        for chunk in chunks(data, 0x34)
    ]


def read_address(address):
    # Requires patched firmware to read use.
    return [
        Packet(pack("<BBBBI", 0x12, 0x20, 0x00, 0x00, address))
    ]


def set_leds(data):
    packets = []
    colorIndex = 0

    for packetIndex in range(0, 0xF, 2):
        packet = bytearray(64)
        pack_into("<BBB", packet, 0, 0x51, 0xA8, packetIndex)

        for i in range(0, 16 * 3, 3):
            pack_into("<BBB", packet, 4 + i, data[colorIndex + 0], data[colorIndex + 1], data[colorIndex + 2])
            colorIndex += 3
        
        packets.append(Packet(packet, delay=0))

    return packets