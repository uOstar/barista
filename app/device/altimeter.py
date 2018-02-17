from app.utils.i2c import I2C
from time import sleep

MPL3115A2_ADDRESS = 0x60
STATUS = 0x00
OUT_P_MSB = 0x01
OUT_P_DELTA_CSB = 0x08
OUT_P_DELTA_MSB = 0X07
OUT_T_MSB = 0x04
WHOAMI = 0x0C
CTRL_REG1 = 0x26
PT_DATA_CFG = 0x13
BAR_IN_MSB = 0x14

class Altimeter (object):

    def __init__(self):

        while(True):
            try:
                self.bus = I2C(1, MPL3115A2_ADDRESS)
                #Set oversample rate to 128
                current_setting = self.bus.read_byte(CTRL_REG1)
                new_setting = 0xb8
                self.bus.write_byte(MPL3115A2_ADDRESS, CTRL_REG1, new_setting)
                break

            except IOError:
                print("Device not connected.")
                sleep(3)

        # Enable event flags
        self.bus.write_byte(MPL3115A2_ADDRESS, PT_DATA_CFG, OUT_P_DELTA_MSB)

        # Toggel One Shot
        setting = self.bus.read_byte(MPL3115A2_ADDRESS, CTRL_REG1)
        if (setting & 0x02) == 0:
            self.bus.write_byte(MPL3115A2_ADDRESS, CTRL_REG1, (setting | 0x02))



    def read(self):
        raw_data = self.bus.read_block(MPL3115A2_ADDRESS, OUT_P_MSB, 3)
        return Altimeter.parse_raw_data(raw_data)



    def read_bar_setting(self):
        setting = self.bus.read_block(MPL3115A2_ADDRESS, BAR_IN_MSB, 2)
        print("Current \t" + str(setting))
        return setting



    def write_bar_setting(self, input):
        hex_input = hex(input)
        self.bus.write_block(MPL3115A2_ADDRESS, BAR_IN_MSB, input)
        setting = read_bar_setting()
        print("New: \t" + str(setting))
        return (setting == input)



    @staticmethod
    def parse_raw_data(raw_data):
        alt_int_bin = raw_data[0] + raw_data[1] + raw_data[2][0] + raw_data[2][1]
        alt_frac_bin = raw_data[2][2] + raw_data[2][3]

        alt_int = 262144-int(alt_bin,2) + 1
        alt_frac = (3-int(alt_frac_bin,2) +1)/4.0
        #Pressure integer part
        altitude = alt_int + alt_frac
        return altitude