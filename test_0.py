import subprocess
from PIL import ImageGrab
import time
import pywinauto
import cv2 as cv
import numpy
from collections import deque
from threading import Thread


class PairList:
    def __init__(self):
        self.this_deque = deque([None, None])

    def add(self, item):
        self.this_deque.rotate()
        self.this_deque.pop()
        self.this_deque.append(item)

    def get(self):
        return self.this_deque[0], self.this_deque[1]


class Breakout:

    Y_TARGET = 517

    def __init__(self):
        subprocess.Popen(
            '"C:/Users/ben/Downloads/bgb/bgb.exe" -rom "C:/Users/ben/Downloads/VisualBoyAdvance-1.8.0-beta3/Alleyway (JUE) [!].gb"')
        tasklist = [line.split() for line in subprocess.check_output("tasklist").splitlines()][1:]
        item = [task for task in tasklist if b'bgb' in task[0]]
        self.pid = int(item[0][1])
        self.coords = {'ball': (224, 182, 224 + 336, 182 + 384)
                       , 'paddle': (224, 515, 224 + 336, 513 + 21)}
        self.templates = {'ball': cv.imread('C:/Users/ben/Documents/screens/ball.png', 0)
                          , 'paddle': cv.imread("C:/Users/ben/Documents/screens/paddle.png", 0)}
        self.pair_list = PairList()
        self.desired_paddle_position = 50

    def _screen_grab(self, coords):
        screen = ImageGrab.grab(coords)
        return screen

    def bring_up(self):
        app = pywinauto.application.Application().connect(process=self.pid)
        app.top_window().set_focus()

    def _save_screen(self):
        screen = self._screen_grab(self.main_coords)
        screen.save('C:/Users/ben/Documents/screens/test' + str(int(time.time())) + '.png')

    def start(self):
        press(RETURN, .2)
        time.sleep(6)
        self.move_paddle()

    def get_item_position(self, item):
        screen = self._screen_grab(self.coords[item]).convert('L')
        screen = numpy.array(screen)
        template = self.templates[item]
        w, h = template.shape[::-1]
        method = cv.TM_SQDIFF_NORMED
        res = cv.matchTemplate(screen, template, method)
        if numpy.min(res) > .1:
            return 0
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return top_left, bottom_right

    def get_midpoint(self, point):
        return int((point[0][0] + point[1][0]) / 2), int((point[0][1] + point[1][1]) / 2)

    def predict(self):
        point_1, point_2 = self.pair_list.get()
        m = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        if m > 0:
            return
        b = point_1[1] - m*point_1[0]
        x_target = (Breakout.Y_TARGET - b) / m
        return x_target

    def _in_play(self):
        press(S, .1)
        time.sleep(1)
        self.pair_list.add(self.get_item_position('ball'))
        self.pair_list.add(self.get_item_position('ball'))
        while True:
            if self.get_item_position('ball'):
                while self.get_item_position('ball'):
                    if self.predict():
                        x_target = self.predict()
                        self.desired_paddle_position = x_target
            time.sleep(.05)

    def _move_paddle(self):
        while True:
            current_position = self.get_midpoint(self.get_item_position('paddle'))[0]
            move = self.desired_paddle_position - current_position
            hold = abs(move/10 * 0.03)
            if move > 0:
                press(R, hold)
            else:
                press(E, hold)
            time.sleep(.05)

    def move_paddle(self):
        Thread(target=self._move_paddle).start()

    def in_play(self):
        Thread(target=self._in_play).start()





bo = Breakout()
bo.bring_up()
time.sleep(3)
bo.start()

time.sleep(2)
bo.in_play()
x = bo.get_item_position('ball')
y = bo.get_item_position('paddle')
print(x)
print(y)

bo._save_screen()


def get_midpoint(point):
    return int((point[0][0] + point[1][0]) / 2), int((point[0][1] + point[1][1]) / 2)

get_midpoint(y)[0]