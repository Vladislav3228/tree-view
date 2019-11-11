class Neighbors():
    #Конструктор может принимать неограниченное кол-во аргументов (названий столбцов текущей таблицы (вида представления дерева) )
    def __init__(self, *args):
        for column in args:
            self.__ancestor = column

"""
cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'student'")
        row = cursor.fetchone()
        while row is not None:
            column_names.append(row[0])
            row = cursor.fetchone()
"""

def Hello():
    print('hello, genius!')