import sqlite3 as lite
from os import getcwd


# сохрение в файл
def save_data(filename, data_rodes, data_nodes):
    con = lite.connect(filename)
    cur = con.cursor()
    with con:
        # удаляем таблицу стержней, если она существует
        cur.execute('DROP TABLE IF EXISTS Rods')
        # создаём таблицу стержней
        cur.execute('CREATE TABLE Rods(№ INTEGER, L INTEGER, A INTEGER, E INTEGER, σ INTEGER, q INTEGER);')
        # заполняем
        for key in data_rodes:
            cur.execute("INSERT INTO Rods(№, L, A, E, σ, q) VALUES(%s, %s, %s, %s, %s, %s)"
                        % (key, data_rodes[key][0], data_rodes[key][1], data_rodes[key][2],
                           data_rodes[key][3], data_rodes[key][4]))

        # удаляем таблицу узлов, если она существует
        cur.execute('DROP TABLE IF EXISTS Nodes')
        # создаём таблицу узлов
        cur.execute('CREATE TABLE Nodes(№ INTEGER, F INTEGER, Заделка Boolean);')
        # заполняем
        for key in data_nodes:
            cur.execute("INSERT INTO Nodes(№, F, Заделка) VALUES(%s, %s, %s)"
                        % (key, data_nodes[key][0], data_nodes[key][1]))


def get_data(filename):
    con = lite.connect(filename)
    cur = con.cursor()
    data_rodes = ()
    data_nodes = ()
    with con:
        try:
            # делаем запрос к таблицам стержней и узлов
            data_rodes = tuple(cur.execute('SELECT * FROM Rods'))
            data_nodes = tuple(cur.execute('SELECT * FROM Nodes'))
        except lite.OperationalError:
            pass

    return data_rodes, data_nodes

# сохранение расчётов
def save_res(Nx, Ux, sigma):
    initial_dir = getcwd()
    con = lite.connect(getcwd() + '\\res.db')
    cur = con.cursor()
    with con:
        cur.execute('DROP TABLE IF EXISTS Rods')
        cur.execute('DROP TABLE IF EXISTS Nx')
        cur.execute('CREATE TABLE Nx(№ INTEGER, Val1 FLOAT, Val2 FLOAT);')

        cur.execute('DROP TABLE IF EXISTS Ux')
        cur.execute('CREATE TABLE Ux(№ INTEGER, Val FLOAT);')

        cur.execute('DROP TABLE IF EXISTS sigma')
        cur.execute('CREATE TABLE sigma(№ INTEGER, Val1 FLOAT, Val2 FLOAT);')

        for index, val in enumerate(Nx):
            cur.execute('INSERT INTO Nx(№, Val1, Val2) VALUES (%s, %.2f, %.2f)' % (index + 1, val[0], val[1]))

        for index, val in enumerate(Ux):
            cur.execute('INSERT INTO Ux(№, Val) VALUES (%s, %.2f)' % (index + 1, val))

        for index, val in enumerate(sigma):
            cur.execute('INSERT INTO sigma(№, Val1, Val2) VALUES (%s, %.2f, %.2f)' % (index + 1, val[0], val[1]))
