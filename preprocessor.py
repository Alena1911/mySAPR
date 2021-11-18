from os import getcwd
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from rodstable import Rodstable
from nodestable import Nodestable
from construction import Construction
from savedata import save_data, get_data


class PreprocessorWin(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(expand=YES, fill=BOTH)

        self.master.title('Препроцессор')
        self.make_widgets()

    # положение виджетов
    def make_widgets(self):
        inner = Innerframe(self.parent)
        inner.pack(side=BOTTOM)
        con = Construction(self)
        con.pack(side=TOP)
        PreprocessMenu(self.parent, inner, con)

# верхнее меню
class PreprocessMenu:
    def __init__(self, parent, inner_fr, con):
        self.menu_bar = Menu()
        self.parent = parent
        self.parent.config(menu=self.menu_bar)

        self.bottom_btns = inner_fr
        self.construction = con

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Файл', menu=self.file_menu)

        self.file_menu.add_command(label='Открыть', command=lambda self=self: self.bottom_btns.open_file())
        self.file_menu.add_command(label='Сохранить', command=lambda self=self: self.bottom_btns.save_file())

        self.parameters = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Параметры', menu=self.parameters)

        self.rods_param = Menu(self.parameters, tearoff=0)
        self.parameters.add_cascade(label='Стержни', menu=self.rods_param)

        self.nodes_param = Menu(self.parameters, tearoff=0)
        self.parameters.add_cascade(label='Узлы', menu=self.nodes_param)

        self.rods_param.add_command(label='Пронумеровать стержни', command=self.rod_number)

        self.rods_param.add_command(label='Показать нагрузки', command=self.q_force)

        self.nodes_param.add_command(label='Пронумеровать узлы', command=self.node_number)

        self.nodes_param.add_command(label='Показать силы', command=self.force)

        self.parameters.add_command(label='Дополнительные параметры', command=self.show_other_param)
        #self.parameters.add_command(label='Очистить всё', command=lambda self=self: self.construction.clear_all())

    # отображение дополнительных параметров
    def show_other_param(self):
        if not self.construction.cv.gettags('other'):
            self.construction.draw_l_line()
            self.construction.draw_ea_line()
            if not self.construction.cv.gettags('axes'):
                self.construction.draw_axes_system()
            else:
                self.construction.cv.delete('axes')
        else:
            self.construction.cv.delete('other')

    # отображение номеров стержней
    def rod_number(self):
        if not self.construction.cv.gettags('rod_numb'):
            self.construction.draw_number_rod()
        else:
            self.construction.cv.delete('rod_numb')

    # нагрузки
    def q_force(self):
        if not self.construction.cv.gettags('q'):
            self.construction.draw_q_force()
        else:
            self.construction.cv.delete('q')

    # номера узлов
    def node_number(self):
        if not self.construction.cv.gettags('node_numb'):
            self.construction.draw_number_node()
        else:
            self.construction.cv.delete('node_numb')
    # силы F
    def force(self):
        if not self.construction.cv.gettags('force'):
            self.construction.draw_force()
        else:
            self.construction.cv.delete('force')

# отображение нижних кнопок
class Innerframe(Frame):

    flag = False

    def __init__(self, parent=None):
        Frame.__init__(self, parent, width=640, height=120)
        self.pack(expand=YES, fill=BOTH)

        self.make_widgets()

    def make_widgets(self):
        # self.opn_file_btn = Button(self, text='Открыть файл', font=('Times', 10, 'italic bold'),
        #                         command=self.open_file)
        # self.opn_file_btn.pack(side=LEFT, expand=YES, fill=BOTH)
        #
        # self.save_file_btn = Button(self, text='Сохранить в файл', font=('Times', 10, 'italic bold'),
        #                             command=self.save_file)
        # self.save_file_btn.pack(side=LEFT, expand=YES, fill=BOTH)

        self.rodes_btn = Button(self, text='Параметры стержней', font=('Times', 12),
                               command=self.open_rods_win)
        self.rodes_btn.pack(side=LEFT, expand=YES, fill=BOTH)

        self.nodes_btn = Button(self, text='Параметры узлов', font=('Times', 12),
                                command=self.open_nodes_win)
        self.nodes_btn.pack(side=LEFT, expand=YES, fill=BOTH)

        # открыть редактор стержней
    def open_rods_win(self):
        Rodstable(Toplevel(self)).mainloop()
        # открыть редактор узлов
    def open_nodes_win(self):
        Nodestable(Toplevel(self)).mainloop()

        # выгрузка из файла
    def open_file(self):
        filename = askopenfilename(parent=self, defaultextension='.db', filetypes=[('Database', '.db')],
                                   initialdir='C:\\')
        save_filename = open(getcwd() + '\\filepath.txt', 'w')
        save_filename.write(filename)
        rods, nodes = get_data(filename)

        Rodstable.fill_dict(rods)
        Nodestable.set_dict(nodes)

        # сохранение в файл
    def save_file(self):
        flag = True
        filename = asksaveasfilename(parent=self, defaultextension='.db', filetypes=[('Database', '.db')],
                                   initialdir='C:\\')
        save_filename = open(getcwd() + '\\filepath.txt', 'w')
        save_filename.write(filename)
        rods = Rodstable.get_data_about_rods()
        nodes = Nodestable.get_data_about_nodes()
        save_data(filename, rods, nodes)




if __name__ == '__main__':
    PreprocessorWin(Tk()).mainloop()

