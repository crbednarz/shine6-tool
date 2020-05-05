from pywinusb import hid
from time import sleep

# 21 x 6
KeyLayout = [
    96, -1, 97, 98, 99, 104, 105, 106, 112, 113, 114, 67, 68, 69, 102, 103, 107, 110, 111, 109, 108,
    0, 1, 8, 9, 16, 17, 24, 25, 32, 33, 40, 41, 48, 49, 56, 57, 64, 72, 73, 80, 81,
    2, 3, 10, 11, 18, 19, 26, 27, 34, 35, 42, 43, 50, 51, 58, 59, 66, 74, 75, 82, 83,
    4, 5, 12, 13, 20, 21, 28, 29, 36, 37, 44, 45, -1, 52, -1, -1, -1, 76, 77, 84, -1,
    6, -1, 7, 14, 15, 22, 23, 30, 31, 38, 39, 46, -1, 47, -1, 61, -1, 78, 79, 86, 85,
    91, 90, 92, -1, -1, -1, 93, -1, -1, -1, 94, 95, 60, 54, 63, 62, 70, -1, 71, 87, -1]


class Keyboard:
    def __init__(self, flash_mode=False, callback=None):
        keyboard = Keyboard._findDevice(flash_mode)
        keyboardIn = keyboard.find_input_reports()
        keyboardOut = keyboard.find_output_reports()

        self._device = keyboard
        self._input = keyboardIn[0]
        self._output = keyboardOut[0]
        self.callback = None
        if callback:    
            keyboard.set_raw_data_handler(callback)

    @staticmethod
    def _findDevice(flash_mode):
        product_id = 0x1203 if flash_mode else 0x0203
        filter = hid.HidDeviceFilter(vendor_id = 0x04d9, product_id = product_id)
        hid_device = filter.get_devices()
        device = hid_device[0]
        device.open()
        return device

    def send_packets(self, packets):
        for packet in packets:
            self._send_packet(packet)

    def _send_packet(self, packet):
        self._output.set_raw_data([0] + list(packet.data))
        self._output.send()
        sleep(packet.delay)

    def close(self):
        self._device.close()