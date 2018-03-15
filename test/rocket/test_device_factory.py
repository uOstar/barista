import pytest
from mock import patch

from app.device.accelerometer import Accelerometer
from app.device.brakes import Brakes
from app.device.gps import GPS
from app.device.gyro import Gyro
from app.device.parachute import Parachute

from app.rocket.device_factory import DeviceFactory

@patch.object(Accelerometer, '__init__')
@patch.object(Brakes, '__init__')
@patch.object(GPS, '__init__')
@patch.object(Gyro, '__init__')
@patch.object(Parachute, '__init__')
def test_init_creates_one_of_each_device(accelerometer_mock, brakes_mock, gps_mock, gyro_mock, parachute_mock):
    accelerometer_mock.return_value = None
    brakes_mock.return_value = None
    gps_mock.return_value = None
    gyro_mock.return_value = None
    parachute_mock.return_value = None

    device_factory = DeviceFactory()

    assert accelerometer_mock.called
    assert brakes_mock.called
    assert gps_mock.called
    assert gyro_mock.called
    assert parachute_mock.called
