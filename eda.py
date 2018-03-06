# this file will be used to determine velocity of the paddle

time.sleep(2)
data = list()
for i in numpy.arange(0, 1, .03):
    length = i
    press(R, length)
    y = bo.get_item_position('paddle')
    z = bo.get_midpoint(y)
    datum = (length, z)
    press(E, .75)
    data.append(datum)

# it looks like roughly .03 seconds moves roughly 10 pixels
