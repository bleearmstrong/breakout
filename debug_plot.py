import random
import numpy
from matplotlib import pyplot as plt
import time

fig, ax = plt.subplots(subplot_kw={'xlim': [0, 336],
                                   'ylim': [-384, 0]})

plt.ion()
points = bo.ball_history
for i in range(len(points) - 1):
    x_1, y_1 = points[i]
    y_1 = -y_1
    x_2, y_2 = points[i + 1]
    y_2 = -y_2
    x_3 = bo.paddle_history[i + 1]
    x_4 = bo.desired_paddle_position_history[i + 1]
    p1, = ax.plot(x_1, y_1, 'bo') # creates a blue dot
    p2, = ax.plot(x_2, y_2, 'ro')
    p3, = ax.plot(x_3, -340, 'g^', markersize=22)
    p4, = ax.plot(x_4, -340, 'm^', markersize=22)
    plt.show()
    plt.pause(.2)
    p1.remove()
    p2.remove()
    p3.remove()
    p4.remove()


bo.paddle_history
bo.desired_paddle_position_history