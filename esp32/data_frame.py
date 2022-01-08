from exception import *
from util import cal_dcs

class DataFrame:
    head = b'\x00\x00\xff'

    def __init__(self, tfi: bytes, pds: bytes) -> None:
        self.tfi = tfi
        self.pds = pds

    def to_bytes(self) -> bytes:
        if len(self.tfi) + len(self.pds) == 0:
            return b'\x00\x00\xff\x00\xff\x00'
        datas = bytearray(self.tfi + self.pds)
        dcs = cal_dcs(datas)
        length = len(datas)
        # print(datas, length)
        lcs = 256 - length
        return self.head + bytearray((length, lcs)) + datas + bytearray((dcs, 00))

    @classmethod
    def from_bytes(cls, b: bytes):
        if b[:3] != cls.head or b[-1] != 0 or len(b) < 6:
            raise InvalidFrameError

        length = b[len(cls.head)]
        lcs = b[len(cls.head) + 1]
        if length == 0 and lcs == 255 and len(b) == 6:
            return DataFrame(b'', b'')
        elif length + lcs != 256 or len(b) != 7 + length:
            raise InvalidFrameError
        else:
            datas = b[len(cls.head) + 2:-2]
            dcs = cal_dcs(datas)
            if dcs != b[-2]:
                raise InvalidFrameError
            return DataFrame(datas[0:1], datas[1:])
