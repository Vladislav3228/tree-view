import random

class Neighbors():

    def __init__(self, cursor, columns, tableName):
        self._ancestor = columns[0]
        self._descendant = columns[1]
        self._tableName = tableName
        self._cursor = cursor
    
    def del_node(self, a):
        # Получаем всех потомков нашей вершины и записываем их в массив
        subtree = []
        self._cursor.execute("SELECT " + self._descendant + " FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a))
        res = self._cursor.fetchone()
        while res is not None:
            subtree.append(res[0])
            res = self._cursor.fetchone()

        # Узнаем предка (Q) нашей вершины 'a'
        self._cursor.execute("SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(a))
        Q = self._cursor.fetchone()[0]

        # удаляем нашу вершину, а ребра от нее к своим потомкам перекидываем на ее предка (Q)
        for node in subtree:
            self._cursor.execute("UPDATE " + self._tableName + " SET " + self._ancestor + " = " + str(Q) + ", " + self._descendant + " = " + str(node) + " WHERE " + self._ancestor + " = " + str(a) + " AND " + self._descendant + " = " + str(node))
        self._cursor.execute("DELETE FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(a))
    
    def del_sbtr(self, a):
        #узнаем потомков нашей вершины и вызываем от них рекурсивно этот же метод
        self._cursor.execute("SELECT " + self._descendant + " FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a))
        m = []
        res = self._cursor.fetchone()
        while res is not None:
            m.append(res[0])
            res = self._cursor.fetchone()

        for i in m:
            self.del_sbtr(i)

        #удаляем все ребра нашей вершины (удаляем нашу вершину)
        self._cursor.execute("DELETE FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a) + " OR " + self._descendant + " = " + str(a))

    # a - куда, b - вставляемая вершина
    def insert(self, a, b):
        #проверка на то, что вставляемой на данный момент вершины не существует
        self._cursor.execute("SELECT COUNT(" + self._descendant + ") FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(b))
        if self._cursor.fetchone()[0] != 0:
            print("такая вершина уже существует!")
        else:
            self._cursor.execute("INSERT INTO " + self._tableName + " VALUES (" + str(a) + ", " + str(b) + ")")

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def move_sbtr(self, a, b):
        self._cursor.execute("SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(a))
        Q = self._cursor.fetchone()[0]
        self._cursor.execute("UPDATE " + self._tableName + " SET " + self._descendant + " = " + str(a) + ", " + self._ancestor + " = " + str(b) + " WHERE " + self._descendant + " = " + str(a) + " AND " + self._ancestor + " = " + str(Q))

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def move_node(self, a, b):
        self.del_node(a)
        self._cursor.execute("INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES (" + str(b) + ", " + str(a) + ")")

    def random_tree(self, a):
        self._cursor.execute("DELETE FROM " + self._tableName)
        self._cursor.execute("INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES (1, 1)")
        for i in range(1, a):
            self.insert(random.randint(1, i), i+1)

    def getGraph(self, G):
        nodes = set()
        self._cursor.execute("SELECT DISTINCT " + self._ancestor + " FROM " + self._tableName)
        res = self._cursor.fetchone()
        while res is not None:
            nodes.add(res[0])
            res = self._cursor.fetchone()
        self._cursor.execute("SELECT DISTINCT " + self._descendant + " FROM " + self._tableName)
        res = self._cursor.fetchone()
        while res is not None:
            nodes.add(res[0])
            res = self._cursor.fetchone()
        # Выше происходит занесение в массив nodes всех различных вершин

        # Создание всех этих вершин в графе G
        for i in nodes:
            G.add_node(str(i))

        # Создание всех ребер вершин по записям таблицы (предок -> наследник)
        self._cursor.execute("SELECT * FROM " + self._tableName)
        res = self._cursor.fetchone()
        while res is not None:
            G.add_edge(str(res[0]), str(res[1]))
            res = self._cursor.fetchone()

        return G
"""
" + self._tableName + "
" + self._ancestor + "
" + self._descendant + "
"""