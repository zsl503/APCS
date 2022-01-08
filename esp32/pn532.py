from machine import UART
from data_frame import DataFrame
from exception import *
import time

def write_df(uart:UART,df:DataFrame):
    uart.write(df.to_bytes())


class Pn532:
    def __init__(self, tx, rx) -> None:
        self.card_uart = UART(1, baudrate=115200, tx=tx,
                              rx=rx, stop=1, parity=None, bits=8)

    def active(self):
        self.card_uart.write(b'\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        write_df(self.card_uart,DataFrame(b'\xD4',b'\x14\x01'))
        res_df = self.res
        return res_df and res_df.tfi == b'\xD5' and res_df.pds == b'\x15'

    @property
    def res(self) -> DataFrame:
        res = read_data(self.card_uart)
        if res[:6] == b'\x00\x00\xff\xff\x00\x00':
            return None
        elif res[:6] == b'\x00\x00\xff\x00\xff\x00':
            if len(res[6:]) == 0:
                res = read_data(self.card_uart)
            else:
                res = res[6:]
            return DataFrame.from_bytes(res)
        else:
            raise InvalidFrameError

    def get_uid(self) -> Optional[bytes]:
        try:
            write_df(self.card_uart,DataFrame(b'\xD4',b'\x4A\x02\x00'))
            res_df = self.res
            return res_df.pds[-4:]
        except WaitReplyTimeOutError as e:
            return None

    def verify(self, block_id:int, passwd:bytes, uid:bytes) ->bool:
        write_df(self.card_uart,DataFrame(b'\xD4',b'\x40\x01\x60' + block_id.to_bytes(1,'little',False) + passwd + uid))
        res_df = self.res
        if res_df.pds == b'\x41\x00':
            return True
        else:
            return False

    def read_card(self,block_id) ->bytes:
        write_df(self.card_uart,DataFrame(b'\xD4',b'\x40\x01\x30' + block_id.to_bytes(1,'little',False)))
        res_df = self.res
        if res_df.tfi != b'\xD5' or res_df.pds[:2] != b'\x41\x00':
            return None
        else:
            return res_df.pds[2:]


def read_data(uart: UART, length=None, timeout: int = 2):
    start = time.time()
    end = start
    while uart.any() == 0 and end - start < timeout:
        end = time.time()

    if uart.any() == 0:
        raise WaitReplyTimeOutError
    if length:
        return uart.read(length)
    else:
        return uart.read()


def write_df(uart:UART,df:DataFrame):
    uart.write(df.to_bytes())


if __name__ == '__main__':
    pn = Pn532(tx=25, rx=26)
    pn.active()
    uid = pn.get_uid()
    if uid is not None:
        veri = pn.verify(9,b'\xff\xff\xff\xff\xff\xff',uid)
        print('verify',pn.read_card(8))

    else:
        print('No card')
