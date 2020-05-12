import click
import time
from Shine6 import commands as cmd
from Shine6.keyboard import open_keyboard


@click.command()
@click.option('--output-file', '-o', help='Output file for flash dump.')
def main(output_file):
    """Dumps all memory from keyboard."""
    is_capturing = False
    dump = []
    def capture_bytes(data):
        if is_capturing:
            dump.extend(data[5:5+0x3c])

    with open_keyboard(callback=capture_bytes) as keyboard:
        keyboard.send_packets(cmd.lock_settings())
        packets = []
        for address in range(0x00, 0xa428, 0x3c):
            packets += cmd.read_address(address)
        is_capturing = True
        keyboard.send_packets(packets)
        is_capturing = False

        keyboard.send_packets(cmd.unlock_settings())
        time.sleep(1)


    with open(output_file, 'wb') as file:
        file.write(bytearray(dump[:0xa428]))

if __name__ == '__main__':
    main()