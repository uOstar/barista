require 'beaglebone'

class Device::Accelerometer
  include Beaglebone

  I2C_ADDR = 0x53

  def read
    puts read_i2c(6, 0x1D)
  end

  def sleep
    new_register = read_i2c(1, 0x3E) | 0b01000000
    write(0x3E, new_register)
  end

  def wake
    new_register = read_i2c(1, 0x3E) | 0b01000000
    write(0x3E, new_register)
  end

  private

  def write_i2c(register, data)
    i2c_gyro.write(I2C_ADDR, [register, data].pack('C*'))
  end

  def read_i2c(bytes, start_address)
    i2c_gyro.read(I2C_ADDR, bytes, [start_address].pack('C*'))
  end

  def i2c_gyro
    @i2c_gyro ||= I2CDevice.new(:I2C2)
  end
end
