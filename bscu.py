#!/usr/bin/env python3
import binascii
import os

from ctypes import *


class SaveFile:
    """Represents the Super Smash Bros. savefile (only tested with PAL)

    Args:
        directory (str): Path to decrypted SSBB savefile folder
    """

    class AutoSave(BigEndianStructure):
        _pack_ = 1
        _fields_ = [
            ("unknown1", ARRAY(c_byte, 0x15B0)),
            ("goldenHammers", c_uint8),
            ("unknown2", ARRAY(c_byte, 0xB0CB))
        ]

        def calculate_checksum(self):
            return binascii.crc32(bytes(self)).to_bytes(4, "big")

        def pack(self):
            return bytes(self)

        def pack_with_checksum(self):
            return self.pack() + self.calculate_checksum()

        def __str__(self):
            output = "AutoSave:\n"
            output += "  Golden Hammers: {0}\n".format(self.goldenHammers)
            output += "  Checksum: {0}\n".format(binascii.hexlify(self.calculate_checksum()).decode())

            return output

    class Net(BigEndianStructure):
        _fields_ = [
            ("unknown", ARRAY(c_byte, 0x281C))
        ]

        def calculate_checksum(self):
            return binascii.crc32(bytes(self)).to_bytes(4, "big")

        def pack(self):
            return bytes(self)

        def pack_with_checksum(self):
            return self.pack() + self.calculate_checksum()

        def __str__(self):
            output = "Net:\n"
            output += "  Checksum: {0}\n".format(binascii.hexlify(self.calculate_checksum()).decode())

            return output

    def __init__(self, directory):
        self.directory = directory
        autosave_file = []
        net_file = []
        for i in range(2):
            try:
                autosave_file.append(open(os.path.join(self.directory, "autosv{0}.bin".format(i)), "rb").read())
            except FileNotFoundError:
                raise FileNotFoundError("autosv{0}.bin not found".format(i))

            try:
                net_file.append(open(os.path.join(self.directory, "net{0}.bin".format(i)), "rb").read())
            except FileNotFoundError:
                raise FileNotFoundError("net{0}.bin not found".format(i))

        self.autosave = []
        for num, autosave in enumerate(autosave_file):
            if len(autosave) != 50816:
                raise Exception("This is not a valid autosv{0}.bin!".format(num))
            self.autosave.append(self.AutoSave.from_buffer_copy(autosave))
            self.autosave[num].checksum = autosave[-4:]
            if self.autosave[num].calculate_checksum() != self.autosave[num].checksum:
                print("WARNING: autosv{0}.bin CRC32 checksum mismatch!".format(num))

        if autosave_file[0] != autosave_file[1]:
            print("WARNING: autosv0.bin is NOT THE SAME as autosv1.bin!")

        self.net = []
        for num, net in enumerate(net_file):
            if len(net) != 10272:
                raise Exception("This is not a valid net{0}.bin!".format(num))
            self.net.append(self.Net.from_buffer_copy(net))
            self.net[num].checksum = net[-4:]
            if self.net[num].calculate_checksum() != self.net[num].checksum:
                print(self.net[num].calculate_checksum())
                print(self.net[num].checksum)
                print("WARNING: net{0}.bin CRC32 checksum mismatch!".format(num))

        if net_file[0] != net_file[1]:
            print("WARNING: net0.bin is NOT THE SAME as net1.bin!")

    def set_golden_hammers(self, num):
        """Sets golden hammers from 0 to 255.
           NOTE: More than 5 will glitch the milestone wall.
        """
        if not 255 >= num >= 0:
            raise ValueError("Minimum is 0, maximum is 255.")

        for autosave in self.autosave:
            autosave.goldenHammers = num
        self.update_autosave_checksum()

    def update_autosave_checksum(self):
        """Updates checksum of the autosave file."""
        for num, autosave in enumerate(self.autosave):
            with open(os.path.join(self.directory, "autosv{0}.bin".format(num)), "wb") as autosave_file:
                autosave_file.write(autosave.pack_with_checksum())

    def update_net_checksum(self):
        """Updates checksum of the net file."""
        for num, net in enumerate(self.net):
            with open(os.path.join(self.directory, "net{0}.bin".format(num)), "wb") as net_file:
                net_file.write(net.pack_with_checksum())

    def update_checksums(self):
        self.update_autosave_checksum()
        self.update_net_checksum()

    def __str__(self):
        output = "Super Smash Bros. Brawl Savefile\n"
        for num, autosave in enumerate(self.autosave):
            if autosave.calculate_checksum() != autosave.checksum:
                output += "  WARNING: AutoSave{0} checksum mismatch!\n".format(num)

        if self.autosave[0].pack() != self.autosave[1].pack():
            output += "  WARNING: autosv0.bin is NOT THE SAME as autosv1.bin!\n"

        output += "\n"
        output += str(self.autosave[0])
        output += "\n"
        output += str(self.net[0])

        return output
