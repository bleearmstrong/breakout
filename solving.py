

def get_line(points):
    x_1, y_1 = points[0]
    x_2, y_2 = points[1]
    m = (y_2 - y_1) / (x_2 - x_1)
    b = y_2 - m*x_2
    return m, b


def flip_points(points):
    return tuple((tup[0], -tup[1]) for tup in points)


def done(line, t, w):
    m, b = line
    x = (-t - b) / m
    return 0 < x < w


def down(points):
    return points[0][1] > points[1][1]


def predict(points, t, w):
    points = flip_points(points)
    line = get_line(points)
    i = 0
    while not done(line, t, w) and i < 100:
        print(line)
        m, b = line
        if down(points):
            if m > 0:
                line = -m, b
            else:
                collision_point = w, m * w + b
                m = -m
                b = collision_point[1] - m * collision_point[0]
                line = m, b
        else:
            if 0 < -b / m < w:
                collision_point = -b / m, 0
                m = -m
                b = collision_point[1] - m * collision_point[0]
                line = m, b
            else:
                collision_point = w, m * w + b
                m = -m
                b = collision_point[1] - m * collision_point[0]
                line = m, b
        i += 1
    m, b = line
    print(line)
    return (-t - b) / m


these_points = ((20, 10), (22, 6))
predict(these_points, 90, 100)