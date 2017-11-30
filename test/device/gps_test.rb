require 'minitest/autorun'
require_relative '../../app/device/gps'

class Device::GpsTest < MiniTest::Test

  def setup
  end

  def test_parse
    assert_equal(1,gps.new().gps_parse('GPGGA,194530.000,3051.8007,N,10035.9989,W,1,4,2.18,746.4,M,-22.2,M,,*6B'))
  end
  def test_read
    assert_equal(1,gps.new().gps_parse(gps.new().gps_read()))
  end
  
  def test_write
  end
end
