import click
import time
from Shine6 import commands as cmd
from Shine6.keyboard import Keyboard


def capture_bytes(data):
    print(f"Raw data: {data}")


@click.command()
def main():
    """Dumps all memory from keyboard."""
    keyboard = Keyboard(callback=capture_bytes)
    keyboard.send_packets(cmd.lock_settings())
    packets = []
    for address in range(0x100, 0xb000, 0x34):
        packets += cmd.read_address(address)
    keyboard.send_packets(packets)

    keyboard.send_packets(cmd.unlock_settings())
    time.sleep(1)
    keyboard.close()

if __name__ == '__main__':
    main()