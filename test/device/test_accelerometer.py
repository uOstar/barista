import pytest
from app.device.accelerometer import Accelerometer


def test_not_moving():
#sample data while not moving
    raw_data = [18, 0, 4, 0, 234, 0]

#parsed sample data
    expected_data ={
        'x_acceleration': 0.0702,
        'z_acceleration': 0.9828,
        'y_acceleration': 0.0156,
        'time': 1518136213.101481
    }
    assert Accelerometer.parse_raw_data(raw_data) == expected_data
