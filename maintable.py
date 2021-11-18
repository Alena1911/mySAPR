from tkinter import *
from tkinter.ttk import Treeview


GENERAL_FONT = ('Times', 14)

# описание кнопки Готово
class Readybutton(Button):
    def __init__(self, parent=None):
        Button.__init__(self, parent, text='Готово', font=GENERAL_FONT)

# отрисовка полей ввода стержней
class Entrysrods(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=YES)

        self.numb_lbl = Label(self, text='№')
        self.numb_entry = Entry(self, width=33)

        self.length_lbl = Label(self, text='L')
        self.length_entry = Entry(self, width=33)

        self.a_lbl = Label(self, text='A')
        self.a_entry = Entry(self, width=33)

        self.e_lbl = Label(self, text='E')
        self.e_entry = Entry(self, width=33)

        self.sigma_lbl = Label(self, text='[σ]')
        self.sigma_entry = Entry(self, width=32)

        self.q_lbl = Label(self, text='q')
        self.q_entry = Entry(self, width=32)



        self.place_widgets()
    
    # положение виджетов на окне
    def place_widgets(self):
        self.numb_lbl.grid(row=1, column=0)
        self.numb_entry.grid(row=0, column=0)

        self.length_lbl.grid(row=1, column=1)
        self.length_entry.grid(row=0, column=1)

        self.a_lbl.grid(row=1, column=2)
        self.a_entry.grid(row=0, column=2)

        self.e_lbl.grid(row=1, column=3)
        self.e_entry.grid(row=0, column=3)

        self.sigma_lbl.grid(row=1, column=4)
        self.sigma_entry.grid(row=0, column=4)

        self.q_lbl.grid(row=1, column=5)
        self.q_entry.grid(row=0, column=5)

        #self.ready_btn.grid(row=2, column=0)


# отрисовка кнопок Добавить/Удалить
class Tablebuttons(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.ready_btn = Readybutton(self)
        #self.plus_btn = Button(self, text='Добавить', font=GENERAL_FONT)
        self.minus_btn = Button(self, text='Удалить', font=GENERAL_FONT)

        self.place_widgets()
    # положение кнопок на окне
    def place_widgets(self):
        #self.plus_btn.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.minus_btn.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.ready_btn.pack(side=LEFT, expand=NO, fill=BOTH)

# отрисовка полей ввода узлов
class Entrysnodes(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.numb_lbl = Label(self, text='№')
        self.numb_entry = Entry(self, width=33)

        self.force_lbl = Label(self, text='F')
        self.force_entrys = Entry(self, width=33)

        self.var = IntVar()

        self.obstacle_check = Checkbutton(self, text='Опора', variable=self.var)
        #self.ready_btn = Readybutton(self)

        self.place_widgets()

    # положение виджетов на окне
    def place_widgets(self):
        self.numb_lbl.grid(row=1, column=0)
        self.numb_entry.grid(row=0, column=0)

        self.force_lbl.grid(row=1, column=1)
        self.force_entrys.grid(row=0, column=1)

        self.obstacle_check.grid(row=0, column=2, padx=65)

        #self.ready_btn.pack(side=LEFT, expand=YES, fill=BOTH)
        #self.ready_btn.grid(row=2, column=0, side=LEFT, sticky=SE)

#Таблица
class Table(Frame):
    def __init__(self, parent, title, columns):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)

        self.title_lbl = Label(self, text=title, font=GENERAL_FONT)
        self.table_tree = Treeview(self, columns=columns)

        #self.scroll = Scroll(self, orient=VERTICAL, command=self.table_tree.yview)
        #self.table_tree['yscroll'] = self.scroll.set

        for i in range(len(columns)):
            self.table_tree.heading(columns[i], text=columns[i])

        self.place_widgets()

    def place_widgets(self):
        self.title_lbl.pack(side=TOP, fill=X, expand=YES)
        self.table_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        #self.scroll.pack(side=RIGHT, fill=Y, expand=YES)

if __name__ == '__main__':
    Entrysnodes().mainloop()

