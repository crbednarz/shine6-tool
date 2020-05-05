import hashlib
from struct import unpack_from, unpack, pack_into, pack


# This XOR key acts as a second layer of encryption for the firmware.
# (Special thanks to https://github.com/ChaoticConundrum/pok3r_re_firmware for making me realize an xor encryption was being used)
# To find the key I made some assuptions:
# 0 is almost always the most common value.
# 0 ^ key = key
# The xor key was 52-bits

# Using this, I built a key using the most common values, and looked at the result.
# There were several places were words were visible, but partially corrupted.
# By attempting the 2nd, 3rd, and 4th most common values for those parts of the key, I was able to piece together
# all key pieces except for 3.
#
# From there I noticed a pattern at the start of the file, where "6f 35 00 00" repeated several times, and used that as reference
# to correct the last few key pieces.
V1_02_10_XOR_KEY = [
    0xE7C29474,
    0x79084B10,
    0x53D54B0D,
    0xFC1E8F32,
    0x48E81A9B,
    0x773C808E,
    0xB7483552,
    0xD9CB8C76,
    0x2A8C8BC6,
    0x0967ADA8,
    0xD4520F5C,
    0xD0C3279D,
    0xEAC091C5]


def xor_52_bit_apply(data, xorKey):
    for i in range(0, len(data), 4):
        (unpackedValue, ) = unpack_from("<I", data, i)
        unpackedValue ^= xorKey[(i // 4) % 13]
        pack_into("<I", data, i, unpackedValue)



def shuffle_decrypt(data):
    # As a base-line encryption, bytes and then bits are shuffled.
    # Presumably to stop people from finding the firmware without reverse engineering the code.

    for i in range(4, len(data), 5):
        (data[i], data[i - 4]) = (data[i - 4], data[i])

    for i in range(1, len(data), 2):
        (data[i], data[i - 1]) = (data[i - 1], data[i])

    for i in range(0, len(data)):
        a = data[i]
        d = a
        d -= 7
        d <<= 4
        a >>= 4
        d += a
        data[i] = d & 0xFF


class UpdaterReader:
    def __init__(self, filePath):
        self._fileData = []

        with open(filePath, 'rb') as fileHandle:
            self._fileData = fileHandle.read()
        
        fileHash = hashlib.md5(self._fileData).hexdigest()
        
        if fileHash != '6dc65ce3ab32a4d0002aa4f5848431a1':
            raise Exception('Hash for %s (%s) is not recognized.' % (filePath, fileHash))


        # These values were taken from reverse engineering the v1.02.10 FWUpdate.exe
        # Most of the data here is extracted from sub_404390 which can be found by looking for a
        # reference to the UTF-16 string "Fail to find firmware information!"
        
        # The loop found in UpdaterReader.parseMetadataTags is pretty close to the original assembly, and it shouldn't be hard to find
        # where values were lifted from.
        self._xorKey = V1_02_10_XOR_KEY
        self._metadataReadOffset = 2760
        self._metadataSize = 0x0b24
        self._metadataOffsetFromEoF = 2852
        self._metadataTagSeparation = 80
        self._metadataTagCount = 9
        self._firmwares = {}
        self._parse_file()

    
    def _parse_file(self):
        metadataStart = len(self._fileData) - self._metadataOffsetFromEoF

        self._metadata = bytearray(self._fileData[metadataStart : metadataStart + self._metadataSize])
        shuffle_decrypt(self._metadata)
        self._find_firmwares()

    def _find_firmwares(self):
        # The metdata section of FWUpdate.exe is actually a series of tags/values.

        fileIndex = len(self._fileData) - self._metadataOffsetFromEoF
        metadataIndex = self._metadataReadOffset
        
        for _ in range(0, self._metadataTagCount):
            
            (dataLength, versionLength, name) = unpack_from("<ii72s", self._metadata, metadataIndex)
            fileIndex -= versionLength
            
            name = name.decode('utf-16')
            version = ""
            data = bytearray()

            if versionLength != 0:
                versionBuffer = bytearray(self._fileData[fileIndex : fileIndex + versionLength])
                shuffle_decrypt(versionBuffer)
                version = versionBuffer.decode("utf-16")

                # Version and name are null terminated utf-16 strings. So we need to clip off the end
                version = version[2:version.index('\0\0')]
                name = name[:name.index('\0\0')]

            fileIndex -= dataLength

            if dataLength != 0:
                valueBuffer = bytearray(self._fileData[fileIndex : fileIndex + dataLength])
                shuffle_decrypt(valueBuffer)
                xor_52_bit_apply(valueBuffer, self._xorKey)
                data = valueBuffer

            metadataIndex -= self._metadataTagSeparation

            if versionLength != 0:
                self._firmwares[f"{name} {version}"] = data
            

    def save_firmwares(self, path):
        for key, value in self._firmwares.items():
            with open(f"{path}/{key}.dat", 'wb') as file:
                file.write(value)