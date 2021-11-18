# модуль представляющий результаты расчёта в виде таблиц QTableWidget с использованием PyQt5
from os import getcwd
from PyQt5.QtGui import QFont
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3 as lite


class MyTable(QWidget):
    # класс представляющий результаты расчёта в виде таблиц

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Таблицы расчётов')
        con = lite.connect(getcwd() + '\\res.db')
        with con:
            cur = con.cursor()
            self.Ux = tuple(cur.execute('SELECT * FROM Ux'))
            self.Nx = tuple(cur.execute('SELECT * FROM Nx'))
            self.sigma = tuple(cur.execute('SELECT * FROM sigma'))

        self.table_Nx = QTableWidget(len(self.Nx), 2)
        self.table_Nx.setHorizontalHeaderLabels('№;Значение'.split(';'))

        self.table_Ux = QTableWidget(len(self.Ux), 2)
        self.table_Ux.setHorizontalHeaderLabels('№;Значение'.split(';'))

        self.table_sigma = QTableWidget(len(self.sigma), 2)
        self.table_sigma.setHorizontalHeaderLabels('№;Значение'.split(';'))

        # лейблы
        self.lbl_Nx = QLabel('<b>N</b><sub><b>x</b></sub>')
        self.lbl_Ux = QLabel('<b>U</b><sub><b>x</b></sub>')
        self.lbl_sigma = QLabel('<b>σ</b>')
        self.lbl_Nx.setFont(QFont('Times', 12))
        self.lbl_Ux.setFont(QFont('Times', 12))
        self.lbl_sigma.setFont(QFont('Times', 12))

        # основные layouts
        self.vbox_Nx = QVBoxLayout()
        self.vbox_Ux = QVBoxLayout()
        self.vbox_sigma = QVBoxLayout()
        self.general_vbox = QHBoxLayout()

        self.place_widgets()
        self.setdata()

        # модифицировать внешний вид таблиц
        self.change_facade()

    # расположение элементов
    def place_widgets(self):
        # Nx - таблица
        self.vbox_Nx.addStretch(1)
        self.vbox_Nx.addWidget(self.lbl_Nx)
        self.vbox_Nx.addWidget(self.table_Nx)

        # Ux - таблица
        self.vbox_Ux.addStretch(1)
        self.vbox_Ux.addWidget(self.lbl_Ux)
        self.vbox_Ux.addWidget(self.table_Ux)

        # sigma - таблица
        self.vbox_sigma.addStretch(1)
        self.vbox_sigma.addWidget(self.lbl_sigma)
        self.vbox_sigma.addWidget(self.table_sigma)

        # главный лайоут
        self.general_vbox.addStretch(1)
        self.general_vbox.addLayout(self.vbox_Nx)
        self.general_vbox.addLayout(self.vbox_Ux)
        self.general_vbox.addLayout(self.vbox_sigma)

        self.setLayout(self.general_vbox)

    # заполение таблиц
    def setdata(self):
        size_Nx = len(self.Nx)
        size_Ux = len(self.Ux)
        size_sigma = len(self.sigma)
        for i in range(size_Nx):
            for j in range(2):
                if j == 0:
                    self.table_Nx.setItem(i, j, QTableWidgetItem('%s' % self.Nx[i][j]))
                else:
                    self.table_Nx.setItem(i, j, QTableWidgetItem('%s, %s' % (self.Nx[i][j], self.Nx[i][j + 1])))

        for i in range(size_Ux):
            for j in range(2):
                self.table_Ux.setItem(i, j, QTableWidgetItem('%s' % self.Ux[i][j]))

        for i in range(size_sigma):
            for j in range(2):
                if j == 0:
                    self.table_sigma.setItem(i, j, QTableWidgetItem('%s' % self.sigma[i][j]))
                else:
                    self.table_sigma.setItem(i, j, QTableWidgetItem('%s, %s' % (self.sigma[i][j], self.sigma[i][j + 1])))

    def change_facade(self):
        self.table_Nx.resizeColumnsToContents()
        self.table_Nx.resizeRowsToContents()
        self.table_Nx.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table_Ux.resizeColumnsToContents()
        self.table_Ux.resizeRowsToContents()
        self.table_Ux.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table_sigma.resizeColumnsToContents()
        self.table_sigma.resizeRowsToContents()
        self.table_sigma.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # расширение столбцов и строк на всё содержимое лайоута
        h_header_Nx = self.table_Nx.horizontalHeader()
        h_header_Nx.setStretchLastSection(True)
        v_header_Nx = self.table_Nx.verticalHeader()
        v_header_Nx.setStretchLastSection(True)
        v_header_Nx.setVisible(False)

        h_header_Ux = self.table_Ux.horizontalHeader()
        h_header_Ux.setStretchLastSection(True)
        v_header_Ux = self.table_Ux.verticalHeader()
        v_header_Ux.setStretchLastSection(True)
        v_header_Ux.setVisible(False)

        h_header_sigma = self.table_sigma.horizontalHeader()
        h_header_sigma.setStretchLastSection(True)
        v_header_sigma = self.table_sigma.verticalHeader()
        v_header_sigma.setStretchLastSection(True)
        v_header_sigma.setVisible(False)

        self.lbl_Nx.setAlignment(Qt.AlignCenter)
        self.lbl_Ux.setAlignment(Qt.AlignCenter)
        self.lbl_sigma.setAlignment(Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table = MyTable()
    table.show()

    sys.exit(app.exec_())
