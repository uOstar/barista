from app.utils.i2c import I2C
from time import sleep
from time import time
import numpy as np
import logging
from smbus2 import SMBus #temp


ADDRESS = 0x77
#I2C address byte
addr_byte = 0xEE
# cmd
read_all = 0x20
read_gyro = 0x21
read_accel = 0x22
read_compass = 0x23
read_temp_c = 0x2B
read_temp_f = 0x2C

read_all_filtered = 0x25
read_gyro_filtered = 0x26
read_accel_filtered = 0x27
read_compass_filtered = 0x28
read_linear_accel = 0x29
read_gyro_filtered_rad_s = 0x26
read_accel_filtered_g = 0x31


class IMUs(object):


    def __init__(self):
        self.i2c = I2C(1, ADDRESS)
        # reset sensor settings
        # self.i2c.write_byte(addr_byte, 0xE0)


    def get_slave_status(self):
        self.i2c. write_byte(addr_byte, 0x41)
        return self.i2c. read_byte(addr_byte)


    def send_command(self,command,param=0x00):
        self.i2c.write_byte(addr_byte, 0x42)
        self.i2c.write_byte(command, param)


    #@staticmethod
    def read(self,bytes):
        self.i2c.write_byte(addr_byte, 0x43)
        data = self.i2c.read_block(0x00, bytes) ##TODO: maybe???
        return data


    #sample sensor read functions
    def read_temp_c(self):
        self.send_command(0x2B)
        return float(self.i2c.byte_array_to_float32(self.read(4)))


    def read_accel_filtered(self):
        self.send_command(0x27)
        return self.read(12)


if __name__ == '__main__':
    #do something
