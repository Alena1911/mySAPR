from tkinter.messagebox import showerror
from preprocessor import *
from processor import *
from postprocessor import *

COLOR = '#000000'
WIDTH = 640
HEIGHT = 480
FONT = ('Verdana', 20)


class MainWindow(Frame):
    def __init__(self, parent=None, color=COLOR):
        Frame.__init__(self, parent)
        self.master.title('Главное окно')
        self.pack()

        self.cv = Canvas(self, width=WIDTH, height=HEIGHT, bg=color)
        self.cv.pack()

        self.make_widgets()

    def make_widgets(self):
        fr = Frame(self, width=180, height=150, bg=COLOR)
        fr.pack()
        self.cv.create_window(320, 250, window=fr)

        self.prebtn = Button(fr, text='Препроцессор',
                             font=FONT, command=self.make_preprocessorwin)
        self.prebtn.pack(expand=YES, fill=BOTH)

        self.prbtn = Button(fr, text='Процессор', font=FONT, state=DISABLED,
                            command=self.make_processorwin)

        self.prbtn.pack(expand=YES, fill=BOTH, pady=15)

        self.postprbtn = Button(fr, text='Постпроцессор', font=FONT, state=DISABLED,
                                command=self.make_postprocessorwin)
        self.postprbtn.pack(expand=YES, fill=BOTH)

    def make_preprocessorwin(self):
        win = Toplevel(self)
        win.protocol('WM_DELETE_WINDOW', lambda win=win, self=self: self.make_active(win, 1))
        PreprocessorWin(win).mainloop()

    def make_active(self, win, type):
        win.destroy()
        if type == 1:
            if not Nodestable.dict_items or not Rodstable.dict_items:
                pass
            else:
                self.prbtn['state'] = 'normal'
        else:
            self.postprbtn['state'] = 'normal'

    def make_processorwin(self):
        filename = open(getcwd() + '\\filepath.txt').readline()
        print(filename)
        if not filename:
            showerror('Ошибка', 'Не могу найти данные для расчёта', parent=self)
            return
        win = Toplevel(self)
        win.protocol('WM_DELETE_WINDOW', lambda win=win, self=self: self.make_active(win, 2))
        ProcessorWin(win, filename).mainloop()

    def make_postprocessorwin(self):
        PostprocessorWin(Toplevel(self)).mainloop()


if __name__ == '__main__':
    root = Tk()
    MainWindow(root)
    root.mainloop()
