
from machine import Pin
import time
class Computer:
    def __init__(self):
        self.__pin_status = Pin(17, Pin.IN, Pin.PULL_DOWN)
        self.__pin_open = Pin(16, Pin.OUT)
        self.__pin_reset = Pin(27, Pin.OUT)

    def update_status(self):
        if self.__pin_status.value() == 1:
            self.__status = True
        else:
            self.__status = False
        time.sleep_ms(10)

    @property
    def status(self):
        if self.__pin_status.value() == 1:
            return True
        else:
            return False

    def open(self):
        if self.status is False:
            self.__pin_open.value(1)
            time.sleep(1)
            self.__pin_open.value(0)

    def close(self):
        if self.status:
            self.__pin_open.value(1)
            time.sleep(8)
            self.__pin_open.value(0)

    def reset(self):
        if self.status:
            self.__pin_reset.value(1)
            time.sleep(1)
            self.__pin_reset.value(0)


if __name__ == "__main__":
    #pin_open = Pin(16, Pin.OUT)
    #pin_open.value(1)
    #print(pin_open.value())
    #time.sleep(1)
    #pin_open.value(0)
    computer = Computer()
    print(computer.status)
    computer.reset()