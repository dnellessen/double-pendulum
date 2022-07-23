from math import sin, cos, pi

class Pendulum:
    def __init__(self, length1=1, length2=1, mass1=1, mass2=1, theta1=pi/2, theta2=pi/2, trace_lenght=100):
        '''
        Create a pendulum object.

        Physics: https://web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

        Parameters
        ----------
        length1 : int, default 1
            Length of the first rod.
        length2 : int, default 2
            Length of the second rod.

        mass1 : int, default 1
            Mass attached to the first rod.
        mass2 : int, default 1
            Mass attached to the second rod.

        theata1 : int, default pi/2
            Angle between center and first mass.
        theata2 : int, default pi/2
            Angle between first mass and second mass.

        trace_lenght : int, default 100
            Length of the trace.
        '''

        self.l1, self.l2 = length1, length2
        self.m1, self.m2 = mass1, mass2
        self.theta1, self.theta2 = theta1, theta2

        self.v1, self.v2 = 0, 0
        self.g = 9.81
        self.dt = 0.01
        # time step (and interval) was optained by comparing the time per frame with a timer

        self.trace = []
        self.trace_lenght = trace_lenght


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

    def update_trace(self, x2, y2):
        ''' Updates trace and returns list of its x and y values. '''

        self.trace.append((x2, y2))
        xt = [point[0] for point in self.trace]
        yt = [point[1] for point in self.trace]

        # self.trace_lenght = -1 for infinite trace.
        if len(self.trace) > self.trace_lenght and self.trace_lenght != -1:
            self.trace.remove(self.trace[0])
        return xt, yt

