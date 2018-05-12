from time import sleep
import serial
import logging

class GPS(object):
    def __init__(self):
        self.ser = serial.Serial(port = '/dev/ttyAMA0', baudrate=9600)
        self.set_data_rate(0.2)
        self.set_datatype('GPRMC_GPGGA')

        sleep(1)
        self.ser.flushInput()
        logging.info('GPS Initialized')


    def read(self):
        self.ser.flushInput()

        data1 = self.ser.readline().split(',')
        data2 = self.ser.readline().split(',')
        raw_data = {}

        if data1[0] == '$GPRMC':
            raw_data['GPRMC'] = data1[1:]
            raw_data['GPGGA'] = data2[1:]
        else:
            raw_data['GPRMC'] = data2[1:]
            raw_data['GPGGA'] = data1[1:]
        try:
            return GPS.parse_raw_data(raw_data)
        except Exception as e:
            logging.error('error: {}, raw_data: {}'.format(e, raw_data))
            return { 'fix': False, 'satalites': 0 }


    def set_data_rate(self, rate):
        UPDATE_RATE_MAPPINGS = {
            10: '$PMTK220,10000*2F\r\n',
            5: '$PMTK220,5000*1B\r\n',
            1: '$PMTK220,1000*1F\r\n',
            0.2: '$PMTK220,200*2C\r\n',
        }
        MEASURE_RATE_MAPPINGS = {
            10: '$PMTK300,10000,0,0,0,0*2C\r\n',
            5: '$PMTK300,5000,0,0,0,0*18\r\n',
            1: '$PMTK300,1000,0,0,0,0*1C\r\n',
            0.2: '$PMTK300,200,0,0,0,0*2F\r\n',
        }
        if rate not in UPDATE_RATE_MAPPINGS and MEASURE_RATE_MAPPINGS:
            print 'WARNING: %s is not a valid datarate' % rate

        self.ser.write(UPDATE_RATE_MAPPINGS[rate])
        sleep(1)
        self.ser.write(MEASURE_RATE_MAPPINGS[rate])


    def set_baud_rate(self, rate):
        BAUD_RATE_MAPPINGS = {
            9600: '$PMTK251,9600*17\r\n',
            57600: '$PMTK251,57600*2C\r\n',
        }
        if rate not in BAUD_RATE_MAPPINGS:
            print 'WARNING: %s is not a valid baud rate' % rate

        self.ser.write(BAUD_RATE_MAPPINGS[rate])
        sleep(1)
        self.ser.baudrate = rate
        self.ser.timeout = 2 * rate


    def set_datatype(self, datatype):
        DATATYPE_MAPPINGS = {
            'GPRMC_GPGGA': '$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n',
            'GPRMC': '$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n',
            'None': '$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n',
            'All': '$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n',
        }
        if datatype not in DATATYPE_MAPPINGS:
            print 'WARNING: %s is not a valid datatype' % datatype

        self.ser.write(DATATYPE_MAPPINGS[datatype])


    @staticmethod
    def parse_raw_data(raw_data):
        data = {}
        data['fix'] = bool(int(raw_data['GPGGA'][5])) if raw_data['GPGGA'][5] else False
        data['satelites'] = int(raw_data['GPGGA'][6]) if raw_data['GPGGA'][6] else 0

        if not data['fix']:
            return data

        data['altitude (ASL)'] = float(raw_data['GPGGA'][8]) # meters
        data['time (UTC)']= raw_data['GPRMC'][8][0:2] + ':' + raw_data['GPRMC'][0][2:4] + ':' + raw_data['GPRMC'][0][4:6]

        data['latitude (deg)'] = float(raw_data['GPRMC'][2][0:3])
        data['latitude (min)'] = float(raw_data['GPRMC'][2][3:9])
        data['latitude (dir)'] = raw_data['GPRMC'][3]

        data['longitude (deg)'] = float(raw_data['GPRMC'][4][0:3])
        data['longitude (min)'] = float(raw_data['GPRMC'][4][3:9])
        data['longitude (dir)'] = raw_data['GPRMC'][5]

        data['ground_speed'] = round(float(raw_data['GPRMC'][6]) * 0.514, 3)# m/s

        return data
