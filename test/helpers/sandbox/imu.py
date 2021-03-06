import logging
from time import time

class SandboxIMU(object):
    def __init__(self,imu_data):
        self.sleeping=False
        self.launch_time=None
        self.launched=False
        self.imu_data=imu_data

    def read_temp_c(self):


    def read_orientation_euler(self):
        if self.sleeping:
                    return {
                        'pitch': 0.0,
                        'roll': 0.0,
                        'yaw': 0.0,
                        'time': time()
                    }
                elif self.launched:
                    sample_time = time()
                    simulation_time = sample_time - self.launch_time
                    try:
                        return {
                            'pitch': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Pitch').values[0]),
                            'roll': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Roll').values[0]),
                            'yaw': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Yaw').values[0]),
                            'time': time()
                        }
                    except Exception as e:
                        return {
                        'pitch': self.noise(0.0),
                        'roll': self.noise(0.0),
                        'yaw': self.noise(0.0),
                        'time':time()
                        }
                else:
                    return {
                        'pitch': self.noise(0.0),
                        'roll': self.noise(0.0),
                        'yaw': self.noise(0.0),
                        'time':time()
                    }

    def read_accel_filtered(self):
        if self.sleeping:
            return {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'time': time()
            }
        elif self.launched:
            sample_time = time()
            simulation_time = sample_time - self.launch_time
            try:
                return {
                    'x': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Lateral').values[0]),
                    'y': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Lateral').values[0]),
                    'z': self.noise(self.imu_data.loc[self.imu_data['# Time (s)'] >= simulation_time].iloc[0].filter(like='Vertical').values[0]),
                    'time': sample_time
                }
            except Exception as e:
                return {
                    'x': self.noise(0.0),
                    'y': self.noise(0.0),
                    'z': self.noise(-9.8),
                    'time':time()
                }
        else :
            return {
                'x': self.noise(0.0),
                'y': self.noise(0.0),
                'z': self.noise(-9.8),
                'time':time()
            }


    def sleep(self):
        self.sleeping = True

    def wake(self):
        self.sleeping = False

    def launch(self, start_time):
        self.launched = True
        self.launch_time = start_time

    def reset(self):
        self.launched = False
        self.wake()
        self.launch_time = None

    def noise(self, value):
        return value
