require 'minitest/autorun'
require_relative '../app/device/imu'

class AccelerometerTest < MiniTest::Test

  def setup
    @accelerometer = Device::Accelerometer.new
  end

  def test_read
  end

  def test_write
  end
end
