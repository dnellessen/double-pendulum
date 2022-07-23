import matplotlib.pyplot as plt
import matplotlib.colors as clr
from matplotlib.animation import FuncAnimation

from math import pi
import numpy as np
import threading

from pendulum import Pendulum


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
