import subprocess
from PIL import ImageGrab
import time
import pywinauto
import cv2 as cv
import numpy
from collections import deque
from threading import Thread
import keyboard
import solving
import random
import string


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

    Y_TARGET = 334

    def __init__(self):
        subprocess.Popen(
            '"C:/Users/ben/Downloads/bgb/bgb.exe" -rom "C:/Users/ben/Downloads/VisualBoyAdvance-1.8.0-beta3/Alleyway (JUE) [!].gb"')
        tasklist = [line.split() for line in subprocess.check_output("tasklist").splitlines()][1:]
        item = [task for task in tasklist if b'bgb' in task[0]]
        self.pid = int(item[0][1])
        self.coords = {'ball': (224, 182, 224 + 336, 182 + 384)
                       , 'paddle': (224, 515, 224 + 336, 513 + 21)
                       , 'kill': (201, 106, 201 + 27, 106 + 24)}
        self.templates = {'ball': cv.imread('C:/Users/ben/Documents/screens/ball.png', 0)
                          , 'paddle': cv.imread("C:/Users/ben/Documents/screens/paddle.png", 0)
                          , 'kill': cv.imread("C:/Users/ben/Documents/screens/kill_box.png", 0)}
        self.pair_list = PairList()
        self.desired_paddle_position = 118
        self.kill_box = (203, 106, 203 + 127, 106 + 24)
        self.kill_image = cv.imread('C:/Users/ben/Documents/screens/kill_box.png', 0)


    def _screen_grab(self, coords):
        screen = ImageGrab.grab(coords)
        return screen

    def bring_up(self):
        app = pywinauto.application.Application().connect(process=self.pid)
        app.top_window().set_focus()

    def _save_screen(self, extra=''):
        N = 5
        screen = self._screen_grab(self.coords['ball'])
        screen.save('C:/Users/ben/Documents/screens/test' + str(time.time()) + extra + '.png')

    def start(self):
        keyboard.press(keyboard.RETURN, .2)
        time.sleep(6)

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
        point_1 = self.get_midpoint(point_1)
        point_2 = self.get_midpoint(point_2)
        m = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        if m > 0:
            return
        b = point_1[1] - m*point_1[0]
        x_target = (Breakout.Y_TARGET - b) / m
        print('x_target = ' + str(x_target))
        return x_target

    def _in_play(self):
        keyboard.press(keyboard.S, .1)
        time.sleep(1)
        self.move_paddle()
        self.pair_list.add(self.get_item_position('ball'))
        time.sleep(.25)
        self.pair_list.add(self.get_item_position('ball'))
        i = 0
        while True and self.kill():
            # print(self.pair_list.get())
            if self.get_item_position('ball'):
                while self.get_item_position('ball'):
                    print('predicting: time is ' + str(time.time()))
                    i += 1
                    self.pair_list.add(self.get_item_position('ball'))
                    if i % 2 == 0:
                        self._save_screen(str(self.pair_list.get()[1]))
                    # print(self.pair_list.get())
                    point_1, point_2 = self.pair_list.get()
                    print('point_2 = ' + str(point_2))
                    if point_2 == 0 or point_1 == 0:
                        print('breaking')
                        break
                    if point_1 == point_2:
                        print('continuing')
                        continue
                    point_1 = self.get_midpoint(point_1)
                    print('point_2 = ' + str(point_2))
                    point_2 = self.get_midpoint(point_2)
                    points = (point_1, point_2)
                    if solving.predict(points, w=336, t=334):
                        x_target = solving.predict(points, w=336, t=334)
                        self.desired_paddle_position = x_target
            time.sleep(.05)

    def _move_paddle(self):
        while True and self.kill():
            current_position = self.get_midpoint(self.get_item_position('paddle'))[0]
            move = self.desired_paddle_position - current_position
            if abs(move) < 5:
                continue
            hold = abs(move/10 * 0.03)
            print('desired paddle position is : ' + str(self.desired_paddle_position))
            if move > 0:
                # print('moving R for ' + str(hold) + ' seconds')
                keyboard.press(keyboard.R, hold)
            else:
                # print('moving L for ' + str(hold) + ' seconds')
                keyboard.press(keyboard.E, hold)
            time.sleep(.05)
            print('moving paddle; time is ' + str(time.time()))

    def move_paddle(self):
        Thread(target=self._move_paddle).start()

    def in_play(self):
        Thread(target=self._in_play).start()

    def kill(self):
        return self.get_item_position('kill')





bo = Breakout()
bo.bring_up()
time.sleep(3)
bo.start()

time.sleep(2)
bo.in_play()

bo.pair_list.get()

# x = bo.get_item_position('ball')
# y = bo.get_item_position('paddle')
# print(x)
# print(y)
# bo.bring_up()
# time.sleep(1)
# bo.kill()
#
# bo._save_screen()
#
# bo.pair_list.get()
#
#
# def get_midpoint(point):
#     return int((point[0][0] + point[1][0]) / 2), int((point[0][1] + point[1][1]) / 2)
#
# get_midpoint(y)[0]