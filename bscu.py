#!/usr/bin/env python3
import binascii
import os

from Struct import Struct


class SaveFile:
    """Represents the Super Smash Bros. savefile (only tested with PAL)

    Args:
        directory (str): Path to decrypted SSBB savefile folder
    """

    class AutoSave(Struct):
        __endian__ = Struct.BE

        def __format__(self):
            self.unknown1 = Struct.string(0x15B0)
            self.goldenHammers = Struct.uint8
            self.unknown2 = Struct.string(0xB0CB)

        def calculate_checksum(self):
            return binascii.crc32(self.pack()).to_bytes(4, "big")

        def pack_with_checksum(self):
            return self.pack() + self.calculate_checksum()

        def __str__(self):
            output = "AutoSave\n"
            output += "  Golden Hammers: {0}\n".format(self.goldenHammers)
            output += "  Checksum: {0}\n".format(binascii.hexlify(self.calculate_checksum()).decode())

            return output

    def __init__(self, directory):
        self.directory = directory
        try:
            autosave0_file = open(os.path.join(self.directory, "autosv0.bin"), "rb").read()
            autosave1_file = open(os.path.join(self.directory, "autosv1.bin"), "rb").read()
        except FileNotFoundError:
            raise FileNotFoundError('File not found')

        if len(autosave0_file) != 50816:
            raise Exception("This is not a valid autosv0.bin!")
        if len(autosave1_file) != 50816:
            raise Exception("This is not a valid autosv1.bin!")

        if autosave0_file != autosave1_file:
            print("WARNING: autosv0.bin is NOT THE SAME as autosv1.bin!")

        self.autosave0 = self.AutoSave().unpack(autosave0_file)
        self.autosave0.checksum = autosave0_file[-4:]
        self.autosave1 = self.AutoSave().unpack(autosave1_file)
        self.autosave1.checksum = autosave1_file[-4:]

        if self.autosave0.calculate_checksum() != self.autosave0.checksum:
            print("WARNING: autosv0.bin CRC32 checksum mismatch!")

        if self.autosave1.calculate_checksum() != self.autosave1.checksum:
            print("WARNING: autosv1.bin CRC32 checksum mismatch!")

    def set_golden_hammers(self, num):
        """Sets golden hammers from 0 to 255.
           NOTE: More than 5 will glitch the milestone wall.
        """
        if not 255 >= num >= 0:
            raise ValueError("Minimum is 0, maximum is 255.")

        self.autosave0.goldenHammers = num
        self.autosave1.goldenHammers = num
        self.update_autosave_checksum()

    def update_autosave_checksum(self):
        with open(os.path.join(self.directory, "autosv0.bin"), "wb") as autosave:
            autosave.write(self.autosave0.pack_with_checksum())

        with open(os.path.join(self.directory, "autosv1.bin"), "wb") as autosave:
            autosave.write(self.autosave1.pack_with_checksum())

    def __str__(self):
        output = "Super Smash Bros. Brawl Savefile\n"
        if self.autosave0.calculate_checksum() != self.autosave0.checksum:
            output += "  WARNING: AutoSave0 checksum mismatch!\n"
        if self.autosave1.calculate_checksum() != self.autosave1.checksum:
            output += "  WARNING: AutoSave1 checksum mismatch!\n"

        if self.autosave0.pack() != self.autosave1.pack():
            output += "  WARNING: autosv0.bin is NOT THE SAME as autosv1.bin!\n"

        output += "\n"
        output += str(self.autosave0)

        return output
