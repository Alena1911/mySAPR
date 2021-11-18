from tkinter import *
import rodstable
import nodestable
from tkinter.messagebox import showerror


# класс области отрисовки
class Construction(Frame):
    middle = int()

    # конструктор класса
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.cv = Canvas(self, width=720, height=480, bg='white')
        self.cv.config(scrollregion=(0, 0, 3000, 8000))

        self.sbarX = Scrollbar(self, orient=HORIZONTAL)
        self.sbarX.config(command=self.cv.xview)
        self.cv.config(xscrollcommand=self.sbarX.set)

        self.sbarY = Scrollbar(self, orient=VERTICAL)
        self.sbarY.config(command=self.cv.yview)
        self.cv.config(yscrollcommand=self.sbarY.set)

        self.nodes_coord = []
        self.rods = rodstable.Rodstable.dict_items
        self.nodes = nodestable.Nodestable.dict_items
        self.l_list = []

        self.draw_btn = Button(self, text='Построить',
                               font=('Times', 16))

        self.draw_btn.bind('<Button-1>', self.draw)

        self.place_widgets()

    # положение виджетов
    def place_widgets(self):
        self.draw_btn.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.sbarX.pack(side=BOTTOM, fill=X, expand=YES)
        self.sbarY.pack(side=RIGHT, fill=Y, expand=YES)
        self.cv.pack(side=TOP, fill=BOTH, expand=YES)
        # self.sbar.pack(side=BOTTOM, fill=X)

    # отрисовка кострукции
    def draw(self, event):
        if self.cv.find_all():
            self.clear_all()

        begin_x = 50
        begin_y = 240
        one_a = 100
        h = int()
        for item in self.rods:
            l = 100 * self.rods[item][0]
            h = self.rods[item][1] * one_a

            if item == 1:
                Construction.middle = begin_y + h / 2
            if item >= 2:
                begin_y = Construction.middle - (h / 2)

            self.nodes_coord.append([begin_x, begin_y, h])
            self.l_list.append(l)

            self.cv.create_rectangle(begin_x, begin_y, begin_x + l, begin_y + h, tag='drawing')

            begin_x += l

        self.nodes_coord.append([begin_x, begin_y, h])

        is_block_exists = False

        for val in self.nodes:
            if self.nodes[val][1] != 0:
                if len(self.nodes) > val > 1:
                    showerror('Ошибка', 'Опора может быть только на первом или последнем узле.', parent=self)
                    self.clear_all()
                self.draw_block(val)
                is_block_exists = True
        if not is_block_exists:
            showerror('Ошибка', 'Задаёте хотя бы одну опору.', parent=self)
            self.clear_all()

    # отрисовка сил F
    def draw_force(self):
        for val in self.nodes:
            if self.nodes[val][0] != 0:
                draw_value = self.nodes[val][0]
                x = self.nodes_coord[val - 1][0]
                y = Construction.middle
                if draw_value > 0:
                    self.cv.create_line(x, y, x + 50, y, arrow=LAST, tag='force', fill='blue', width=5)
                else:
                    self.cv.create_line(x - 50, y, x, y, arrow=FIRST, tag='force', fill='blue', width=5)

    # отрисовка опор
    def draw_block(self, numb_node):
        x, y, shift = self.nodes_coord[numb_node - 1]
        if not isinstance(y, int):
            y = int(y)
        if not isinstance(shift, int):
            shift = int(shift)

        end = y + shift + 10
        self.cv.create_line(x, y - 10, x, end, tag='drawing')
        if numb_node == 1:
            for i in range(y - 10, end, 5):
                self.cv.create_line(x, i, x - 5, i + 5, tag='drawing')
        else:
            for i in range(end, y - 10, -5):
                self.cv.create_line(x, i, x + 5, i - 5, tag='drawing')

    # отрисовка номеров стержней
    def draw_number_rod(self):
        y = 100
        for val in range(len(self.rods)):
            x = self.nodes_coord[val][0] - 10
            x += self.l_list[val] / 2
            self.cv.create_oval(x, y, x + 20, y + 20, tag='rod_numb')
            self.cv.create_text(x + 10, y + 10, text='%s' % (val + 1), tag='rod_numb')

    # отрисовка номеров узлов
    def draw_number_node(self):
        for value in range(len(self.nodes)):
            x, y, shift = self.nodes_coord[value]
            y += (shift + 15)
            self.cv.create_rectangle(x + 5, y, x + 25, y + 20, tag='node_numb')
            self.cv.create_text(x + 15, y + 10, text='%s' % (value + 1), tag='node_numb')

    # отрисовка L
    def draw_l_line(self):
        for val in self.rods:
            l = self.l_list[val - 1]
            l_to_draw = self.rods[int(val)][0]
            x, y, shift = self.nodes_coord[val - 1]
            y += shift
            self.cv.create_line(x, y, x, y + 50, tag='other')
            save_x = x

            x += l
            self.cv.create_line(x, y, x, y + 50, tag='other')
            self.cv.create_line(save_x, y + 35, x, y + 35, arrow=BOTH, tag='other')
            self.cv.create_text(save_x + l / 2, y + 25, text='%sL' % l_to_draw, tag='other')

    # отрисовка E и A
    def draw_ea_line(self):
        for obj in self.rods:
            l = self.l_list[obj - 1]
            a = self.rods[obj][1]
            e = self.rods[obj][2]
            x, y, shift = self.nodes_coord[obj - 1]
            x += l / 2
            y += 10
            self.cv.create_line(x, y, x + 20, y - 20, tag='other')
            x += 20
            y -= 20
            self.cv.create_line(x, y, x + 40, y, tag='other')
            self.cv.create_text(x + 20, y - 10, text='%sE, %sA' % ('%.0e' % e, a), tag='other')

    # отрисовка координатной плоскости
    def draw_axes_system(self):
        begin_x = self.nodes_coord[0][0] - 20
        end_x = self.nodes_coord[-1][0] + 30
        y = Construction.middle
        # while begin_x <= end_x:
        #     if begin_x + 10 > end_x:
        #         self.cv.create_line(begin_x, y, begin_x + 5, y, arrow=LAST, tag='axes')
        #     else:
        #         self.cv.create_line(begin_x, y, begin_x + 5, y, tag='axes')
        #     begin_x += 10
        self.cv.create_line(begin_x, y, end_x, y, arrow=LAST, tag='axes')
        self.cv.create_text(end_x, y + 10, text='X', tag='axes')

        begin_y = self.nodes_coord[0][1]
        x = self.nodes_coord[0][0]
        end_y = 50
        # while begin_y >= end_y:
        #     if begin_y - 10 < end_y:
        #         self.cv.create_line(x, begin_y, x, begin_y - 5, arrow=LAST, tag='axes')
        #     else:
        #         self.cv.create_line(x, begin_y, x, begin_y - 5, tag='axes')
        #     begin_y -= 10
        # self.cv.create_line(x, begin_y, x, end_y, arrow=LAST, tag='axes')
        # self.cv.create_text(x + 10, end_y, text='Y', tag='axes')

    # отрисовка нагрузок
    def draw_q_force(self):
        for val in self.rods:
            if self.rods[val][-1] != 0:
                value = self.rods[val][-1]
                x = self.nodes_coord[val - 1][0]
                end_x = x + self.l_list[val - 1]
                while x <= end_x:
                    if x + 20 < end_x:
                        if value > 0:
                            self.cv.create_line(x, Construction.middle, x + 20, Construction.middle, arrow=LAST,
                                                tag='q', fill='red')
                        else:
                            self.cv.create_line(x, Construction.middle, x + 20, Construction.middle, arrow=FIRST,
                                                tag='q', fill='red')
                    else:
                        adder = end_x - x
                        if value > 0:
                            self.cv.create_line(x, Construction.middle, x + adder, Construction.middle, arrow=LAST,
                                                tag='q', fill='red')
                        else:
                            self.cv.create_line(x, Construction.middle, x + adder, Construction.middle, arrow=FIRST,
                                                tag='q', fill='red')
                    x += 20

    # очистка
    def clear_all(self):
        self.cv.delete('drawing')
        self.cv.delete('force')
        self.cv.delete('rod_numb')
        self.cv.delete('node_numb')
        self.cv.delete('other')
        self.cv.delete('axes')
        self.cv.delete('q')
        self.nodes_coord = []
        self.l_list = []


if __name__ == '__main__':
    Construction().mainloop()
