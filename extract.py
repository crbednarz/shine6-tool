import click
from Shine6.extractor import UpdaterReader


@click.command()
@click.option('--input', '-i', default='FWUpdate.exe', help='Path to FWUpdate.exe')
@click.option('--output-dir', '-o', default='.', help='Directory to write unecrypted firmware to.')
def main(input, output_dir):
    updaterFile = UpdaterReader(input)
    updaterFile.save_firmwares(output_dir)
    print("Firmware successfully extracted.")

if __name__ == '__main__':
    main()