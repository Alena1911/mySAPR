from maintable import Table, Tablebuttons, Entrysrods
from tkinter.simpledialog import askinteger
from tkinter.messagebox import showerror, showwarning
from tkinter import *
import nodestable


class Rodstable(Frame):
    count = 0
    dict_items = dict()
    # получение сорваря стержней
    @staticmethod
    def get_data_about_rods():
        return Rodstable.dict_items

    # заполнение словаря стержней 
    @staticmethod
    def fill_dict(data):
        if Rodstable.dict_items:
            Rodstable.dict_items.clear()

        for item in data:
            key = item[0]
            val = item[1:]
            Rodstable.dict_items[key] = val

    # конструктор
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.columns = ('№', 'L', 'A', 'E', 'σ', 'q')
        self.tbl = Table(self, '', columns=('№', 'L', 'A', 'E', 'σ', 'q'))
        self.tbl.table_tree['show'] = 'headings'

        self.entr = Entrysrods(self)
        self.btns = Tablebuttons(self)

        #self.btns.plus_btn.bind('<Button-1>', self.add_new_rode)
        self.btns.minus_btn.bind('<Button-1>', self.delete_rode)

        self.btns.ready_btn.bind('<Button-1>', self.fetch_res)

        self.place_widgets()

        if Rodstable.dict_items:
            self.setter_rodes()

     # положение виджетов
    def place_widgets(self):
        self.tbl.pack()
        self.btns.pack(anchor=SE)

    # очистка таблицы
    def clear_table(self):
        self.tbl.table_tree.delete(*self.tbl.table_tree.get_children())

    #заполенине таблицы
    def fill_table(self):
        for item in sorted(Rodstable.dict_items):
            self.tbl.table_tree.insert('', 'end', iid=item, values=(item, Rodstable.dict_items[item][0],
                                                                    Rodstable.dict_items[item][1],
                                                                    Rodstable.dict_items[item][2],
                                                                    Rodstable.dict_items[item][3],
                                                                    Rodstable.dict_items[item][4]))
    # проверка и запись результатов ввода
    def fetch_res(self, event):
        if self.entr.numb_entry.get():
            try:
                number_rod = int(self.entr.numb_entry.get())
                if not number_rod >= 1:
                    showerror('Ошибка', 'Введён недопустимый № стержня', parent=self)
                    self.entr.numb_entry.delete(0, END)
                    return
            except ValueError:
                showerror('Ошибка', 'Значение должно быть целочисленным', parent=self)
                self.entr.numb_entry.delete(0, END)
                return
        else:
            showwarning('Предупреждение', 'Не введён номер стержня', parent=self)
            if self.entr.length_entry.get():
                self.entr.length_entry.delete(0, END)

            if self.entr.a_entry.get():
                self.entr.a_entry.delete(0, END)

            if self.entr.e_entry.get():
                self.entr.e_entry.delete(0, END)

            if self.entr.sigma_entry.get():
                self.entr.sigma_entry.delete(0, END)

            if self.entr.q_entry.get():
                self.entr.q_entry.delete(0, END)
            return

        if self.entr.length_entry.get():
            try:
                length = float(self.entr.length_entry.get())
                if not length > 0:
                    showerror('Ошибка', 'Длина должна быть > 0', parent=self)
                    self.entr.length_entry.delete(0, END)
                    return
            except ValueError:
                showerror('Ошибка', 'Значение должно быть целочисленным', parent=self)
                self.entr.length_entry.delete(0, END)
                return
        else:
            length = 0

        if self.entr.a_entry.get():
            try:
                a = float(self.entr.a_entry.get())
                if not a > 0:
                    showerror('Ошибка', 'Площадь должна быть > 0', parent=self)
                    self.entr.a_entry.delete(0, END)
                    return
            except ValueError:
                showerror('Ошибка', 'Значение должно быть целочисленным', parent=self)
                self.entr.a_entry.delete(0, END)
                return
        else:
            a = 0

        if self.entr.e_entry.get():
            try:
                e = float(self.entr.e_entry.get())
                if e < 0:
                    showerror('Ошибка', 'E должно быть положительным', parent=self)
                    self.entr.e_entry.delete(0, END)
                    return
            except ValueError:
                showerror('Ошибка', 'Значение должно быть целочисленным', parent=self)
                self.entr.e_entry.delete(0, END)
                return
        else:
            e = 0

        if self.entr.sigma_entry.get():
            try:
                sigma = float(self.entr.sigma_entry.get())
                if not sigma > 0:
                    showerror('Ошибка', 'Допускаемое напряжение должно быть положительным', parent=self)
                    self.entr.sigma_entry.delete(0, END)
                    return
            except ValueError:
                showerror('Ошибка', 'Значение должно быть числом', parent=self)
                self.entr.sigma_entry.delete(0, END)
                return
        else:
            sigma = 0

        if self.entr.q_entry.get():
            try:
                q = float(self.entr.q_entry.get())
            except ValueError:
                showerror('Ошибка', 'Значение должно быть числом', parent=self)
                self.entr.q_entry.delete(0, END)
                return
        else:
            q = 0

        if number_rod in Rodstable.dict_items.keys():
            Rodstable.dict_items[number_rod] = (length, a, e, sigma, q)
            if number_rod <= Rodstable.count:
                self.clear_table()
                self.fill_table()
            else:
                self.tbl.table_tree.delete(number_rod)
                self.tbl.table_tree.insert('', number_rod, iid=number_rod, values=(number_rod, length, a, e, sigma, q))

        else:
            if number_rod > Rodstable.count + 1 and number_rod > 1:
                showerror('Ошибка', 'Введён недопустимый номер стержня', parent=self)
                self.entr.numb_entry.delete(0, END)
                return
                # for i in range(Rodstable.count + 1, number_rod):
                #    Rodstable.dict_items[i] = (0, 0, 0, 0, 0)
                #    self.tbl.table_tree.insert('', i, values=(i, 0, 0, 0, 0, 0))

            Rodstable.dict_items[number_rod] = (length, a, e, sigma, q)
            self.tbl.table_tree.insert('', number_rod, values=(number_rod, length, a, e, sigma, q))

        Rodstable.count = len(Rodstable.dict_items)
        self.set_vals_on_center()

        # добавление нового стержня
    def add_new_rode(self, event):
        Rodstable.count += 1

        self.tbl.table_tree.insert('', 'end', iid=Rodstable.count, values=(Rodstable.count, 0, 0, 0, 0, 0))

        self.set_vals_on_center()

        Rodstable.dict_items[Rodstable.count] = (0, 0, 0, 0, 0)

        # удаление узла
    def delete_rode(self, event):
        if Rodstable.count == 0:
            showerror('Ошибка удаления', 'В таблице не осталось заполненных полей')
            return

        number_to_del = askinteger('', '№ стержня:', parent=self)

        if number_to_del is None:
            return

        if number_to_del not in Rodstable.dict_items:
            showwarning('Предупреждение', 'Попытка удаления несуществующего стержня', parent=self)
            return

        self.clear_table()

        Rodstable.dict_items.pop(number_to_del)
        Rodstable.count -= 1
        for item in Rodstable.dict_items:
            if item > number_to_del:
                Rodstable.dict_items[item - 1] = (Rodstable.dict_items[item][0],
                                                  Rodstable.dict_items[item][1],
                                                  Rodstable.dict_items[item][2],
                                                  Rodstable.dict_items[item][3],
                                                  Rodstable.dict_items[item][4])
                Rodstable.dict_items.pop(item)

        self.fill_table()

     # построение узлов в таблице
    def setter_rodes(self):
        Rodstable.count = len(Rodstable.dict_items)
        self.clear_table()

        self.fill_table()

        self.set_vals_on_center()
    
    # установка значений по центру
    def set_vals_on_center(self):
        for col in self.columns:
            self.tbl.table_tree.column(col, anchor=CENTER)

if __name__ == '__main__':
    Rodstable().mainloop()
