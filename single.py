import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from pendulum import Pendulum

class Animation:
    def __init__(self, pendulum, darktheme=True):
        self.pendulum = pendulum

        facecolor, cpend = ('#000000', '#ededed') if darktheme else ('#ededed', '#000000')
        ctrace = '#5a7d96'

        self.fig = plt.figure(figsize=(4, 4), facecolor=facecolor)
        self.ax = self.fig.gca()

        dif = pendulum.l1 + pendulum.l2 + 0.1
        self.ax.set_xlim((-dif, dif))
        self.ax.set_ylim((-dif, dif))
        self.ax.set_aspect('equal', adjustable='box')

        plt.gcf().canvas.manager.set_window_title('Pendulum')
        plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97)
        plt.axis('off')

        (x1, y1), (x2, y2) = pendulum.coordinates()
        self.pend, = plt.plot((0, x1, x2), (0, y1, y2),
                              color=cpend, marker='o', markersize=3, zorder=1)
        self.trace, = plt.plot(x2, y2, color=ctrace, zorder=0)

    def update(self, frame):
        ''' Update pendulum by setting the updated values to the plot. '''

        self.pendulum.update_values()
        (x1, y1), (x2, y2) = self.pendulum.coordinates()
        xt, yt = self.pendulum.update_trace(x2, y2)

        self.trace.set_data(xt, yt)
        self.pend.set_data((0, x1, x2), (0, y1, y2))

    def run(self):
        anim = FuncAnimation(self.fig, self.update, interval=10.5)
        plt.show()


if __name__ == '__main__':
    pendulum = Pendulum()
    Animation(pendulum).run()
