from time import time


class SandboxAccelerometer(object):


    def __init__(self,acceleration_data):
        self.sleeping = False
        self.launch_time = None
        self.launched = False
        self.acceleration_data = acceleration_data


    def read(self):
        if self.sleeping:
            return{
                'x': 0.0,
                'y': 0.0,
                'z': 0.0,
                'time': time()
                }
        elif self.launched:
            sample_time = time()
            self.simulation_time = sample_time-self.launch_time
            return {
                'x': self.noise(self.acceleration_data.loc[self.acceleration_data['# Time (s)'] >= self.simulation_time].iloc[0].filter(like='Lateral').values[0]),
                'y': self.noise(self.acceleration_data.loc[self.acceleration_data['# Time (s)'] >= self.simulation_time].iloc[0].filter(like='Lateral').values[0]),
                'z': self.noise(self.acceleration_data.loc[self.acceleration_data['# Time (s)'] >= self.simulation_time].iloc[0].filter(like='Vertical').values[0]),
                'time': sample_time
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
        self.sleep()
        self.launch_time = None


    def noise(self, value):
        #TODO: actually return noised value
        return value
