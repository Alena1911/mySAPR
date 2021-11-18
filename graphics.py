# графики для постпроцессора

from tkinter import *
import sqlite3 as lite
from savedata import get_data
import matplotlib.pyplot as plt
from os import getcwd


class General(Frame):
    # общий класс графиков
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.cv = Canvas(self, width=640, height=480, bg='#FFFFFF')
        self.cv.create_line(60, 80, 60, 400)
        self.cv.create_line(60, 240, 580, 240)
        self.cv.create_line(580, 80, 580, 400)
        self.cv.pack()

        self.shifts = []

    def draw_graphic(self, data, param):
        self.draw_axes(param)

        diff_x = 520
        end_x = 580
        y_text = 5
        num_text = 0

        start_x = 60
        for each in data:
            index, val1, val2 = each

            if val1 < 3 or val2 < 3:
                self.cv.create_line(start_x, 240 - int(val1 * 16), self.shifts[index - 1], 240 - int(val2 * 16))
            else:
                self.cv.create_line(start_x, 240 - int(val1), self.shifts[index - 1], 240 - int(val2))
            y_text += 15
            num_text += 1
            self.cv.create_text(63, y_text, text='%s: %s; %s' % (num_text, val1, val2), anchor=NW)

            while start_x < self.shifts[index - 1]:
                if start_x + 10 > self.shifts[index - 1]:
                    break
                start_x += 10
                self.cv.create_line(start_x, 600, start_x, 600 - int(val1))
            if start_x != self.shifts[index - 1]:
                start_x = self.shifts[index - 1]

    def draw_axes(self, param):
        l_list = [val[1] for val in param]

        diff_x = 520
        start_x = 60
        start_y = 80
        end_y = 400
        end_x = 580

        all_parts = sum(l_list)
        for item in l_list:
            shift_x = start_x + diff_x * item // all_parts
            if shift_x > end_x:
                shift_x = end_x
            if end_x - shift_x <= 10:
                shift_x = end_x
            start_x = shift_x
            temp_y = start_y
            while temp_y <= end_y:
                self.cv.create_line(shift_x, temp_y, shift_x, temp_y + 5)
                temp_y += 10
            self.shifts.append(start_x)


class NxGraphic(General):
    def __init__(self, parent=None):
        General.__init__(self, parent)
        self.pack()

        self.master.title('График Nx')

        con = lite.connect(getcwd() + '\\res.db')
        with con:
            cur = con.cursor()
            self.data = tuple(cur.execute('SELECT * FROM Nx'))

        filename = open(getcwd() + '\\filepath.txt').readline().strip()
        self.rods = get_data(filename)[0]

        self.draw()

    def draw(self):
        self.draw_graphic(self.data, self.rods)


class UxGraphic:
    def __init__(self, parent=None):
        con = lite.connect(getcwd() + '\\res.db')
        with con:
            cur = con.cursor()
            self.data = tuple(cur.execute('SELECT * FROM Ux'))

        filename = open(getcwd() + '\\filepath.txt').readline().strip()
        self.nodes = get_data(filename)[1]
        self.draw()

    def draw(self):

        vals = [val[1] for val in self.data]
        j = 0
        Y = []
        while True:
            if j == len(vals):
                break
            if j >= 1:
                if vals[j] > vals[j - 1] or vals[j] < vals[j - 1]:
                    if vals[j] > vals[j - 1]:
                        diff = vals[j] - vals[j - 1]
                        add = diff / 10
                        temp_val = vals[j - 1]
                        while temp_val < vals[j]:
                            Y.append(float('%.2f' % temp_val))
                            temp_val += add
                    else:
                        diff = vals[j - 1] - vals[j]
                        ded = diff / 10
                        temp_val = vals[j - 1]
                        while temp_val > vals[j]:
                            Y.append(float('%.2f' % temp_val))
                            temp_val -= ded
            j += 1

        i = 0.9
        X = []
        while True:
            i += 0.1
            X.append(float('%.2f' % i))
            if i >= self.nodes[-1][0] or len(X) >= len(Y):
                break

        del Y[len(Y) // 2]
        del X[len(X) // 2]
        print(X)
        print()
        print(Y)
        print(len(X))
        print(len(Y))
        if len(X) < len(Y):
            X.append(X[-1])
        if len(Y) < len(X):
            Y.append(Y[-1])
        # X.append(Y[-1])



        plt.plot(X, Y)
        #plt.axis([1, X[-1], 0, max(Y)])
        plt.title('График Ux')
        plt.xlabel('Номер узла')
        plt.ylabel('Перемещение')
        plt.grid()
        plt.show()



class SigmaGraphic(General):
    def __init__(self, parent=None):
        General.__init__(self, parent)
        self.pack()

        self.master.title('График Sigma')

        con = lite.connect(getcwd() + '\\res.db')
        with con:
            cur = con.cursor()
            self.data = tuple(cur.execute('SELECT * FROM sigma'))

        filename = open(getcwd() + '\\filepath.txt').readline().strip()
        self.rods = get_data(filename)[0]

        self.draw()

    def draw(self):
        self.draw_graphic(self.data, self.rods)


if __name__ == '__main__':
    UxGraphic()
