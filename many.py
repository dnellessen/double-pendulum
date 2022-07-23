import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.animation import FuncAnimation

from math import sin, cos, pi

import numpy as np
import threading


class Pendulum:
    def __init__(self, length1=1, length2=1, mass1=1, mass2=1, theta1=pi/2, theta2=pi/2):
        '''https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html'''

        self.l1, self.l2 = length1, length2
        self.m1, self.m2 = mass1, mass2
        self.theta1, self.theta2 = theta1, theta2

        self.v1, self.v2 = 0, 0
        self.g = 9.81
        self.dt = 0.01
        # time step (and interval) was optained by comparing the time per frame with a timer

    def update_values(self):
        '''
        The first dirivitive of theta is the velocity.
        The sencond dirivitive of theta is the acceleration.
        '''

        numerator1 = -self.g * (2*self.m1 + self.m2) * sin(self.theta1) - self.m2 * self.g * sin(self.theta1 - 2*self.theta2) - (2*sin(self.theta1 - self.theta2) * self.m2 * (self.v2**2 * self.l2 + self.v1**2 * self.l1 * cos(self.theta1 - self.theta2)))
        numerator2 = 2*sin(self.theta1 - self.theta2) * (self.v1**2 * self.l1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * cos(self.theta1) + self.v2**2 * self.l2 * self.m2 * cos(self.theta1 - self.theta2))
        denominator = (2*self.m1 + self.m2 - self.m2 * cos(2*self.theta1 - 2*self.theta2))

        a1 = numerator1 / (self.l1 * denominator)
        a2 = numerator2 / (self.l2 * denominator)

        self.v1 += self.dt * a1
        self.v2 += self.dt * a2
        self.theta1 += self.dt * self.v1
        self.theta2 += self.dt * self.v2

    def coordinates(self):
        ''' Returns new coordinates for x1, y1 and x2, y2. '''

        x1 = self.l1 * sin(self.theta1)
        y1 = -self.l1 * cos(self.theta1)

        x2 = x1 + self.l2 * sin(self.theta2)
        y2 = y1 - self.l2 * cos(self.theta2)

        return (x1, y1), (x2, y2)


class Animation:
    def __init__(self, pendulums, darktheme=True):
        self.pendulums_arr = pendulums

        facecolor = '#000000' if darktheme else '#ededed'

        self.fig = plt.figure(figsize=(4, 4), facecolor=facecolor)
        self.ax = self.fig.gca()

        ml1 = max([pendulum.l1 for pendulum in self.pendulums_arr])
        ml2 = max([pendulum.l2 for pendulum in self.pendulums_arr])
        dif = ml1 + ml2 + 0.1
        self.ax.set_xlim((-dif, dif))
        self.ax.set_ylim((-dif, dif))
        self.ax.set_aspect('equal', adjustable='box')

        plt.gcf().canvas.manager.set_window_title('Pendulum(s)')
        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97)
        plt.axis('off')

        # https://matplotlib.org/stable/tutorials/colors/colormaps.html
        cmap = plt.cm.get_cmap('YlOrRd')
        arr = np.linspace(0, 1, len(self.pendulums_arr))
        colors = [clr.rgb2hex(cmap(i)) for i in arr]
            
        self.pendulums = {}
        for i, pendulum in enumerate(self.pendulums_arr):
            (x1, y1), (x2, y2) = pendulum.coordinates()
            pend, = plt.plot((0, x1, x2), (0, y1, y2), color=colors[i])
            self.pendulums[i] = {
                'pendulum': pendulum,
                'plot': pend
            }

    def _individual(self, index):
        ''' Updates a single pendulum by setting the updated values to the plot. '''

        pendulum = self.pendulums[index]
        pendulum['pendulum'].update_values()
        (x1, y1), (x2, y2) = pendulum['pendulum'].coordinates()
        pendulum['plot'].set_data((0, x1, x2), (0, y1, y2))

    def update(self, frame):
        ''' Updates all pendulums with threading. '''

        for index in range(len(self.pendulums)):
            threading.Thread(target=self._individual, args=(index,)).start()

    def run(self):
        anim = FuncAnimation(self.fig, self.update, interval=10.5)
        plt.show()


if __name__ == '__main__':
    pendulums = [Pendulum(theta2=pi/2-i) for i in np.arange(10**-8, 10**-6, 10**-8)]
    Animation(pendulums).run()
