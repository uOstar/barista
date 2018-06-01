from threading import Thread
from collections import deque

import numpy as np
import logging

WINDOW_SIZE = 50

class Kinetics(Thread):
    def __init__(self, device_factory):
        self.imu = device_factory.imu

        self.time_series = deque(np.arange(WINDOW_SIZE), maxlen=WINDOW_SIZE)

        self.acceleration_window = TimeWindow()
        self.velocity_window = TimeWindow()
        self.position_window = TimeWindow()
        self.active = False

    def activate(self):
        if not self.active:
            Thread.__init__(self)
            self.active = True
            self.start()
            if not self.is_alive():
                raise Exception('Failed to activate kinetics model')

    def deactivate(self):
        if self.active:
            self.active = False
            self.join(timeout=1)
            if self.is_alive():
                raise Exception('Failed to deactivate Kinetics Model')

    def predicted_apogee(self):
        accel = self.dict_to_matrix(self.acceleration())
        m = 20 # empty rocket mass
        accel_force = m*accel

        c = self.drag_cofficient()
        area = self.compute_area()
        rho = 2 # mass density of fluid
        b = (1/2)*rho*area*c # nice variable to work with
        velocity = self.dict_to_matrix(self.velocity())
        drag_force = -1*b*np.square(velocity)

        n = np.sqrt(b/accel_force) # another nice variable

        p_burnout = self.position() # TODO: make this return the position at start of TimeWindow
        v_burnout = self.velocity() # TODO: make this return the velocity at start of TimeWindow

        p_apogee = p_burnout - dot((1/((np.square(accel))*(np.sqare(n)))),np.ln(np.cos(np.arctan(2*np.dot(n,v_burnout)))))

        return p_apogee

    def acceleration(self):
        return self.acceleration_window.last()

    def velocity(self):
        return self.velocity_window.last()

    def position(self):
        return self.position_window.last()

    def compute_brakes_percentage(self):
        return 1.0

    def drag_cofficient(self):
        return 1.0

    def compute_area(self):
        return 1.0

    def dict_to_matrix(self, dict):
        return np.array([[dict['x']],
                         [dict['y']],
                         [dict['z']]])

    def run(self):
        while self.active:
            measurement = self.imu.read_accel_filtered()
            self.time_series.append(measurement['time'])
            self.acceleration_window.append(x=measurement['x'], y=measurement['y'], z=measurement['z'])

            prev_velocity = self.velocity_window.last()
            delta_velocity = self.acceleration_window.integrate_last(self.time_series[-2], self.time_series[-1])
            self.velocity_window.append(
                x=prev_velocity['x'] + delta_velocity[0],
                y=prev_velocity['y'] + delta_velocity[1],
                z=prev_velocity['z'] + delta_velocity[2])


            prev_position = self.position_window.last()
            delta_position = self.velocity_window.integrate_last(self.time_series[-2], self.time_series[-1])
            self.position_window.append(
                x=prev_position['x'] + delta_position[0],
                y=prev_position['y'] + delta_position[1],
                z=prev_position['z'] + delta_position[2])

            acceleration = self.acceleration()
            logging.debug("Acceleration x: {}, y: {}, z: {}".format(acceleration['x'], acceleration['y'], acceleration['z']))
            velocity = self.velocity()
            logging.debug("Velocity x: {}, y: {}, z: {}".format(velocity['x'], velocity['y'], velocity['z']))
            position = self.position()
            logging.debug("Position x: {}, y: {}, z: {}".format(position['x'], position['y'], position['z']))

class TimeWindow(object):
    def __init__(self, size=WINDOW_SIZE):
        self.x = deque(np.zeros(size), maxlen=size)
        self.y = deque(np.zeros(size), maxlen=size)
        self.z = deque(np.zeros(size), maxlen=size)

    def append(self, **values):
        self.x.append(values['x'])
        self.y.append(values['y'])
        self.z.append(values['z'])

    def integrate_last(self, t0, t1):
        return np.trapz(
            [[self.x[-2], self.x[-1]],
             [self.y[-2], self.y[-1]],
             [self.z[-2], self.z[-1]]],
            [t0, t1])

    def last(self, count=1):
        if count == 1:
            return {'x': self.x[-1], 'y': self.y[-1], 'z': self.z[-1] }
        else:
            return {'x': self.x[-1:-1*count], 'y': self.y[-1:-1*count], 'z': self.z[-1:-1*count] }
