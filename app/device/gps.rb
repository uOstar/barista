require 'beaglebone'
module Device
  class GPS
  include Beaglebone
  def intiliaze()
    gps = UARTDevice.new(:UART1, 9600)
  end

  def gps_read
    nmea = gps.readline
    return nmea
  end

  def gps_parse(nmea)
    if nmea.include?("GPRMC")
      n1 = nmea.split(",")
      u_in = n1[1].index(".")-2
      p_in = n1[3].index(".")-2
      p2_in = n1[5].index(".")-2

      utc = (n1[1][0..u_in])+(n1[1][u_in..-1]/100)
      signal_stat = n1[2]
      lat1 = l_format(n1[3][0..p_in],n1[3][p_in..-1],n1[4])
      long1 = l_format(n1[5][0..p2_in],n1[5][p2_in..-1],n1[6])
      speed_in_knots = n1[7]
      track_angle= n1[8]
      dmy = n1[9]

    elsif nmea.include?("GPGGA")
      n2 = nmea.split(",")
      u_in = n2[1].index(".")-2
      p_in = n2[2].index(".")-2
      p2_in = n2[4].index(".")-2

      utc2 = (n2[1][0..u_in])+(n2[1][u_in..-1]/100)
      lat2 = l_format(n2[2][0..p_in],n2[2][p_in..-1],n2[3])
      long2 = l_format(n2[4][0..p2_in],n2[4][p2_in..-1],n2[5])
      fix_state = n2[6]
      satellites_amount = n2[7]
      h_dilution = n2[8]
      alt = n2[9]
      a_sea_level = n2[11]
      return fix_state
    end
  end

  def l_format(l,minutes,direction)
    l_return = l+(minutes/60)
    if direction=='N' or direction=='E'
      #do nothing
    else
      l_return = -l_return
    return l_return
    end
  end
end
end
