from i2c import I2C
from time import sleep
from time import time
import numpy as np
class Accelerometer(object):

    ADDRESS = 0x53
    #REGISTERS
    DEVID = 0x00
    BW_RATE = 0x2C # Data rate and power mode control
    POWER_CTL = 0x2D # Power-saving features control
    DATA_FORMAT = 0x31
    DATAX0 = 0x32
    DATAX1 = 0x33
    DATAY0 = 0x34
    DATAY1 = 0x35
    DATAZ0 = 0x36
    DATAZ1 = 0x37


    def __init__(self):
        self.i2c = I2C(1, 0x53)
        #set resolution to 16g
        self.i2c.clear_bit(self.DATA_FORMAT, 1)
        self.i2c.clear_bit(self.DATA_FORMAT, 0)
        #right justify with sign extension
        self.i2c.clear_bit(self.DATA_FORMAT, 2)
        #set maximum resolution mode (4mg/LSB)
        self.i2c.set_bit(self.DATA_FORMAT, 3)
        #set data rate to 3200Hz
        self.i2c.write_byte(self.BW_RATE, 0b00001111)
        #setting the device to measure
        self.i2c.set_bit(self.POWER_CTL, 3)


    def read(self):

        sensor_read = self.i2c.read_block(self.DATAX0,6)
        #block_read returns a list of int

        raw_data = np.int16([
            np.bitwise_or(sensor_read[1] << 8, sensor_read[0]),
            np.bitwise_or(sensor_read[3] << 8, sensor_read[2]),
            np.bitwise_or(sensor_read[5] << 8, sensor_read[4])
        ])

        return Accelerometer.parse_raw_data(raw_data)


    def sleep(self):
        self.i2c.set_bit(self.POWER_CTL, 2)


    def wake(self):
        self.i2c.clear_bit(self.POWER_CTL, 3)
        self.i2c.clear_bit(self.POWER_CTL, 2)
        self.i2c.set_bit(self.POWER_CTL, 3)


    @staticmethod
    def parse_raw_data(raw_data):

        data = {
            'x_acceleration': round(raw_data[0]*0.0039,4),
            'y_acceleration': round(raw_data[1]*0.0039,4),
            'z_acceleration': round(raw_data[2]*0.0042,4),
            'time':time()
        }
        return data


if __name__ == '__main__':
        accelerometer = Accelerometer()
    	print "Benchmarking Accelerometer..."
        start = time()
        for x in range(0,40000):
            accelerometer.read()
        end = time()
        total = end - start
        print accelerometer.read()
        average = total/40000
        print "reading 40000 times took %s seconds total, average of %s seconds per read" %(total,average)
