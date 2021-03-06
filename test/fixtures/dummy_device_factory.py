from time import time
import random
import logging

class DummyIMU(object):
    def __init__(self):
        self.sleeping = False

    def read_accel_filtered(self):
        if self.sleeping:
            return {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'time': time()
            }
        else:
            return {
                'x': round(random.uniform(-10,10),4),
                'y': round(random.uniform(-10,10),4),
                'z': round(random.uniform(-10,10),4),
                'time': time()
            }

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False


class DummyAltimeter(object):
    def __init__(self):
        self.sleeping = False
        self.bar_setting = 1.019

    def read_altitude(self):
        return round(random.uniform(-100,2000),4)

    def get_bar_setting(self):
        return self.bar_setting

    def set_bar_setting(self, bar_setting):
        self.bar_setting = bar_setting

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False

    def reset_bar_input(self):
        return None


class DummyRadio(object):
    ACTION_TRANSITION='transition'
    ACTION_ARM='arm'
    ACTION_TEST_BRAKES='test_brakes'
    ACTION_POSITION_REPORT='position_report'
    ACTION_CONNECTING='connecting'

    def __init__(self):
        self.sleeping = False
        self.action = None
        self.data = None

    def receive(self):
        data = { 'action': str(self.action), 'data': self.data }
        self.data = None
        self.action = None
        return data

    def transmit(self, action, data=None):
        logging.info("Radio transmit: action: {} data: {}".format(action, data))

    def mock_message(self, action, data):
        self.action = action
        self.data = data

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False


class DummyGPS(object):
    def read(self):
        return {
            'fix': True,
            'satelites': 8,
            'time (UTC)': '23:35:19',
            'altitude (ASL)': 545.4,
            'latitude (deg)': 48.0,
            'latitude (min)': 7.038,
            'latitude (dir)': 'N',
            'longitude (deg)': 11.0,
            'longitude (min)': 31.0,
            'longitude (dir)': 'E',
            'ground_speed': 11.514
        }

    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False


class DummyParachute(object):
    def __init__(self):
        self.deployed_stage_one = False
        self.deployed_stage_two = False

    def deploy_stage_one(self):
        logging.info('Deployed Stage One')
        self.deployed_stage_one = True

    def deploy_stage_two(self):
        logging.info('Deployed Stage Two')
        self.deployed_stage_two = True

class DummyBrakes(object):
    def __init__(self):
        self.percentage = 0.0

    def deploy(self, percentage):
        logging.info("Deployed Brakes: {}".format(str(percentage)))
        self.percentage = percentage

class DummyDeviceFactory(object):
    def __init__(self):
        self.imu = DummyIMU()
        self.altimeter = DummyAltimeter()
        self.gps = DummyGPS()
        self.parachute = DummyParachute()
        self.brakes = DummyBrakes()
        self.radio = DummyRadio()

    def sleep_all(self):
        self.imu.sleep()
        self.altimeter.sleep()
        self.gps.sleep()
        self.radio.sleep()

    def wake_all(self):
        self.imu.wake()
        self.altimeter.wake()
        self.gps.wake()
        self.radio.wake()
