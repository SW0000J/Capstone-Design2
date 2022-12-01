#import msgpack
from datetime import date


class Packet:
    def __init__(self, byte
        =b"WW\x00\x0f'\x00\x94\xc42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\xba \xec\x98\xa4\xec\xa0\x84 \x00"):
        self.mData = byte
        # Have to add time in packet

    def SetByteToPacket(self, byte):
        self.mData = byte
        return self.mData

    def SetStringToPacket(self, string):
        self.mData = bytes(string, "utf8")
        return self.mData

    def GetData(self):
        return self.mData

    def __str__(self):
        return str(self.mData)