import bsdiff4
import click
import hashlib


@click.command()
@click.option('--input-file', '-i', help='Path to US v1.02.10 firmware file.')
@click.option('--output-file', '-o', help='Output path for patched firmware.')
def main(input_file, output_file):
    """Patches default firmware to allow reading of any address in memory."""
    with open(input_file, 'rb') as file:
        contents = file.read()

    with open("resources/firmware.patch", 'rb') as file:
        patch = file.read()

    hash = hashlib.sha1(contents).hexdigest()
    
    if hash != '94ffc60b9127e64308b3ce1bc8b81ee11cfc2dff':
        print("Invalid hash for input firmware. Aborting.")
        exit(1)

    patched_firmware = bsdiff4.patch(contents, patch)

    with open(output_file, 'wb') as file:
        file.write(patched_firmware)
    
    print("Patching complete.")


if __name__ == '__main__':
    main()