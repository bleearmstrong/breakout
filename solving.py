

def get_line(points):
    x_1, y_1 = points[0]
    x_2, y_2 = points[1]
    m = (y_2 - y_1) / (x_2 - x_1)
    b = y_2 - m*x_2
    return m, b


def flip_points(points):
    return tuple((tup[0], -tup[1]) for tup in points)


def done(line, t, w, points):
    m, b = line
    x = (-t - b) / m
    return 0 < x < w and down(points)

# done((-1, 1), 90, 100, )

def down(points):
    # print(points)
    # print(points[0])
    # print(points[0][1])
    # print(points[1][1])
    return points[0][1] > points[1][1]


def predict(points, t, w):
    points = flip_points(points)
    line = get_line(points)
    i = 0
    print('********************')
    print('initial line: ', str(line))
    if not done(line, t, w, points):
        print('******************')
        print('initial line didn\'t work')
    while not done(line, t, w, points) and i < 10:
        print('begin bounce')
        print('original line: ', str(line))
        print('direction is down: ' + str(down(points)))
        m, b = line
        if down(points):
            if m > 0:
                print('a')
                line = -m, b
                collision_point = 0, b
                new_point = 1, -m + b
                points = collision_point, new_point
                print('new_points = ' + str(points))
            else:
                print('b')
                collision_point = w, m * w + b
                m = -m
                b = collision_point[1] - m * collision_point[0]
                line = m, b
                new_point = w - 1, m * (w - 1) + b
                points = collision_point, new_point
                print('new_points = ' + str(points))
        else:
            if 0 < -b / m < w:
                print('c')
                collision_point = -b / m, 0
                m = -m
                b = collision_point[1] - m * collision_point[0]
                line = m, b
                adj = 1 if m < 0 else -1
                new_point = (collision_point, ((((collision_point[1] + adj) - b) / m), collision_point[1] + adj))
                points = new_point
                print('new_points = ' + str(points))
            else:
                if m > 0:
                    print('d')
                    collision_point = w, m * w + b
                    m = -m
                    b = collision_point[1] - m * collision_point[0]
                    line = m, b
                    new_point = collision_point[0] + 1, m * (collision_point[0] - 1) + b
                    points = collision_point, new_point
                    print('new_points = ' + str(points))
                else:
                    print('e')
                    collision_point = 0, b
                    m = -m
                    b = collision_point[1] - m * collision_point[0]
                    line = m, b
                    new

        i += 1
        print('collision_point = ' + str(collision_point))
        print((-t - b) / m)
        print('output line', str(line))
        print('**************')
    m, b = line
    print(line)
    return (-t - b) / m


# these_points = ( (10, 9), (8,7))
# print(predict(these_points, 90, 100))
# these_points = ((8,5),(10,10))
# print(predict(these_points, 90, 100))
# down(flip_points(these_points))
