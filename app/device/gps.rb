require 'beaglebone'

class Device::GPS
  include Beaglebone
  def intiliaze()
  end

  gps = UARTDevice.new(:UART1, 9600)
   
  def gps_read
    Nmea = gps.readline
  end

  def gps_parse(Nmea)
    if Nmea.include?("GPRMC")
      N1 = Nmea.split(",")
      U_in = N1[1].index(".")-2
      p_in = N1[3].index(".")-2
      p2_in = N1[5].index(".")-2

      UT2C = (N1[1][0..U_in])+(N1[1][U_in..-1]/100)
      Signal_stat = N1[2]
      Lat1 = L_format(N1[3][0..p_in],N1[3][p_in..-1],N1[4])
      Long1 = L_format(N1[5][0..p2_in],N1[5][p2_in..-1],N1[6])
      speed_in_knots = N1[7]
      track angle= N1[8]
      DMY = N1[9]

    elsif Nmea.include?("GPGGA")
      N2 = Nmea.split(",")
      U_in = N2[1].index(".")-2
      p_in = N2[2].index(".")-2
      p2_in = N2[4].index(".")-2

      UTC2 = (N2[1][0..U_in])+(N2[1][U_in..-1]/100)
      Lat2 = L_format(N2[2][0..p_in],N2[2][p_in..-1],N1[3])
      Long2 = L_format(N2[4][0..p2_in],N2[4][p2_in..-1],N1[5])
      fix_state = N2[6]
      Satellites_amount = N2[7]
      h_dilution = N2[8]
      Alt = N2[9]
      A_Sea_level = N2[11]

  end

  def L_format(l,minutes,direction)
    l_return = l+(minutes/60)
    if direction=='N' or direction=='E'
      pass
    else:
      l_return = -l_return
    return l_return

  end
end
