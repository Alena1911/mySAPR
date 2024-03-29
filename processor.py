from os import getcwd
from tkinter import *
from savedata import get_data, save_res
from tkinter.messagebox import showinfo
import numpy


class ProcessorWin(Frame):
    _ = float('inf')

    def __init__(self, parent=None,
                 filename=getcwd() + '\\test.db'):
        Frame.__init__(self, parent)
        self.master.title('Процессор')
        self.pack()

        self.btns_frame = Frame(self)
        self.calc_btn = Button(self.btns_frame, text='Рассчитать', font=('Times', 20))
        self.show_matrix_btn = Button(self.btns_frame, text='Показать матрицу и векторы', font=('Times', 20),
                                      state=DISABLED)
        self.cancel_btn = Button(self.btns_frame, text='Отмена', font=('Times', 20),
                                 command=self.master.destroy)

        self.calc_btn.bind('<Button-1>', self.calculate)
        self.show_matrix_btn.bind('<Button-1>', self.show_matrix)

        self.place_widgets()

        self.rods, self.nodes = get_data(filename)

        self.size = len(self.nodes)
        self.A = [[0] * self.size for i in range(self.size)]
        self.b = []
        self.N = [0] * len(self.rods)
        self.sigma = [0] * len(self.rods)
        self.Ux = [0 if val[1] == 0 else 1 for val in self.nodes]

    def place_widgets(self):
        self.calc_btn.pack(side=LEFT, expand=YES)
        self.show_matrix_btn.pack(side=LEFT, expand=YES, padx=15)
        self.cancel_btn.pack(side=RIGHT, expand=YES)

        self.btns_frame.pack(side=BOTTOM, anchor=SE)

    def calculate(self, event):
        self.solution()
        showinfo('Информация', 'Расчёт окончен', parent=self)
        self.show_matrix_btn['state'] = NORMAL

    def solution(self):
        self.create_matrix()

        self.create_vector_b()

        # изменение матрицы А с учётом заделок
        blocks = [index for index, val in enumerate(self.nodes) if val[-1] != 0]
        for i in range(self.size):
            for j in range(self.size):
                if i in blocks:
                    if i != j:
                        self.A[i][j] = 0
                    else:
                        self.A[i][j] = 1
                if j in blocks:
                    if i != j:
                        if self.A[i][j] != 0:
                            self.A[i][j] = 0

        if numpy.linalg.det(self.A) != 0:
            reverse_matrix = numpy.linalg.inv(self.A)
            self.Ux = list(numpy.dot(reverse_matrix, self.b))

        self.calculate_Nx()
        self.calculate_sigmax()

        print(self.Ux)
        print(self.N)
        print(self.sigma)

        self.save()

    def create_matrix(self):
        # формирование глобальной матрицы реакций А

        _ = ProcessorWin._
        l_list = [val[1] for val in self.rods]
        a_list = [val[2] for val in self.rods]
        e_list = [val[3] for val in self.rods]

        # p - номер стержня
        # i - номер глобального узла
        # n - число глобальных узлов
        for i in range(self.size):
            for j in range(self.size):
                if i == j or i + 1 == j or i - 1 == j:
                    self.A[i][j] = _

        # формирование глобальной матрицы реакций А(EA/L)
        for i in range(self.size):
            for j in range(self.size):
                if self.A[i][j] == _:
                    if i == j:
                        if i == 0 or i == self.size - 1:
                            if i == 0:
                                self.A[i][j] = e_list[0] * a_list[0] / l_list[0]
                            else:
                                self.A[i][j] = e_list[-1] * a_list[-1] / l_list[-1]
                        else:
                            self.A[i][j] = (e_list[i - 1] * a_list[i - 1] / l_list[i - 1]) + \
                                           (e_list[i] * a_list[i] / l_list[i])
                    else:
                        if i > j:
                            self.A[i][j] = -(e_list[i - 1] * a_list[i - 1] / l_list[i - 1])
                        else:
                            self.A[i][j] = -(e_list[j - 1] * a_list[j - 1] / l_list[j - 1])

    def create_vector_b(self):
        # формирование глобального вектора реакций b
        l_list = [val[1] for val in self.rods]
        q_list = [val[-1] for val in self.rods]
        f_list = [val[1] for val in self.nodes]
        self.b.clear()
        for index, val in enumerate(self.nodes):
            if val[2] == 1:
                one_item = 0
            elif 0 < index < len(self.rods):
                one_item = (q_list[index] * l_list[index] / 2 + f_list[index]) + q_list[index - 1] * l_list[
                    index - 1] / 2
            elif index < len(self.rods):
                one_item = q_list[index] * l_list[index] / 2 + f_list[index]
            else:
                one_item = q_list[index - 1] * l_list[index - 1] / 2 + f_list[index]
            self.b.append(one_item)

    def calculate_Nx(self, x=0):
        # расчёт продольной силы Nx в стержнях

        _ = ProcessorWin._

        l_list = [val[1] for val in self.rods]
        e_list = [val[3] for val in self.rods]
        a_list = [val[2] for val in self.rods]
        q_list = [val[-1] for val in self.rods]
        temp = []
        for i in range(len(self.N)):
            if q_list[i] != 0:
                temp.append(((e_list[i] * a_list[i]) / l_list[i]) * (self.Ux[i + 1] - self.Ux[i]) \
                            + (q_list[i] * l_list[i]) / 2 * (1 - 2 * (x / l_list[i])))
                temp.append(((e_list[i] * a_list[i]) / l_list[i]) * (self.Ux[i + 1] - self.Ux[i]) \
                            + (q_list[i] * l_list[i]) / 2 * (1 - 2 * (l_list[i] / l_list[i])))
                self.N[i] = list(temp)
                temp.clear()
            else:
                self.N[i] = [((e_list[i] * a_list[i]) / l_list[i]) * (self.Ux[i + 1] - self.Ux[i]),
                             ((e_list[i] * a_list[i]) / l_list[i]) * (self.Ux[i + 1] - self.Ux[i])]

    def calculate_sigmax(self):
        a_list = [val[2] for val in self.rods]

        # расчёт напряжения sigma
        for i in range(len(self.N)):
            if len(self.N[i]) > 1:
                self.sigma[i] = [self.N[i][0] / a_list[i], self.N[i][1] / a_list[i]]
            else:
                self.sigma[i] = [self.N[i] / a_list[i], self.N[i] / a_list[i]]

    def show_matrix(self, event):
        new_win = Toplevel(self)
        new_win.title('Матрица и вектор реакций')
        canv = Canvas(new_win, width=500, height=200, bg="#FFFFFF")
        canv.pack(fill=BOTH, expand=YES)

        self.draw_simple(canv)

        # левая -
        canv.create_line(30, 70, 20, 70, width=2)

        start_x = 40
        start_y = 80
        e_list = [val[3] for val in self.rods]

        # матрица реакций А
        for i in range(self.size):
            for j in range(self.size):
                canv.create_text(start_x, start_y, text='%.2f' % self.A[i][j])
                start_x += 40
            start_y += 20
            start_x = 40

        # левая |
        canv.create_line(20, 70, 20, start_y, width=2)
        # левая -
        canv.create_line(20, start_y, 30, start_y, width=2)

        shift_x = start_x * self.size + 10

        # правая -
        canv.create_line(shift_x, 70, shift_x + 10, 70, width=2)
        # правая |
        canv.create_line(shift_x + 10, 70, shift_x + 10, start_y, width=2)
        # правая -
        canv.create_line(shift_x + 10, start_y, shift_x, start_y, width=2)

        shift_x += 30

        # знак умножить
        shift_y = start_y - (start_y - 60) / 2
        canv.create_line(shift_x, shift_y, shift_x + 10, shift_y + 10, width=2)
        canv.create_line(shift_x + 10, shift_y, shift_x, shift_y + 10, width=2)

        # для вектора перемещений
        start_x = shift_x + 60
        start_y = 80
        for item in self.Ux:
            canv.create_text(start_x, start_y, text='%.2f' % item)
            start_y += 20

        # левая { для Ux
        canv.create_text(start_x - 30, 80 + (start_y - 80) / 3, text='{',
                         font=('Courier', start_y - 80, 'normal'))
        # правая } для Ux
        canv.create_text(start_x + 30, 80 + (start_y - 80) / 3, text='}',
                         font=('Courier', start_y - 80, 'normal'))

        # для =
        canv.create_line(start_x + 70, shift_y, start_x + 85, shift_y, width=2)
        canv.create_line(start_x + 70, shift_y + 10, start_x + 85, shift_y + 10, width=2)

        # для вектора b
        start_x += 150
        start_y = 80
        for unit in self.b:
            canv.create_text(start_x, start_y, text='%.2f' % unit)
            start_y += 20

        # левая { для вектора b
        canv.create_text(start_x - 30, 80 + (start_y - 80) / 3, text='{',
                         font=('Courier', start_y - 80, 'normal'))
        # правая } для вектора b
        canv.create_text(start_x + 30, 80 + (start_y - 80) / 3, text='}',
                         font=('Courier', start_y - 80, 'normal'))

    def draw_simple(self, canv):
        linewidth = 2
        canv.create_line(30, 20, 20, 20, width=linewidth)
        canv.create_line(20, 20, 20, 40, width=linewidth)
        canv.create_line(20, 40, 30, 40, width=linewidth)

        canv.create_line(50, 20, 60, 20, width=linewidth)
        canv.create_line(60, 20, 60, 40, width=linewidth)
        canv.create_line(60, 40, 50, 40, width=linewidth)

        my_font = ('Courier', 15, "bold")
        canv.create_text(40, 30, text='A', font=my_font)

        canv.create_line(70, 25, 80, 35, width=linewidth)
        canv.create_line(80, 25, 70, 35, width=linewidth)

        canv.create_text(95, 30, text='{', font=my_font)
        canv.create_text(108, 30, text='Δ', font=my_font)
        canv.create_text(121, 30, text='}', font=my_font)

        canv.create_line(140, 28, 150, 28, width=linewidth)
        canv.create_line(140, 33, 150, 33, width=linewidth)

        canv.create_text(165, 30, text='{', font=my_font)
        canv.create_text(178, 30, text='b', font=my_font)
        canv.create_text(193, 30, text='}', font=my_font)

    def save(self):
        save_res(self.N, self.Ux, self.sigma)


if __name__ == '__main__':
    ProcessorWin(Tk()).mainloop()
