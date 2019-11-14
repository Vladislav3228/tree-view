import random

class Neighbors():
    def __init__(self, cursor, columns, tableName):
        self.__ancestor = columns[0]
        self.__descendant = columns[1]
        self.__tableName = tableName
        self.__cursor = cursor

    def deletion_without_subtree(self, a):
        # Получаем всех потомков нашей вершины и записываем их в массив
        subtree = []
        self.__cursor.execute("SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a))
        res = self.__cursor.fetchone()
        while res is not None:
            subtree.append(res[0])
            res = self.__cursor.fetchone()

        # Узнаем предка (Q) нашей вершины 'a'
        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(a))
        Q = self.__cursor.fetchone()[0]

        # удаляем нашу вершину, а ребра от нее к своим потомкам перекидываем на ее предка (Q)
        for node in subtree:
            self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__ancestor + " = " + str(Q) + ", " + self.__descendant + " = " + str(node) + " WHERE " + self.__ancestor + " = " + str(a) + " AND " + self.__descendant + " = " + str(node))
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(a))
    
    def deletion_with_subtree(self, a):
        #узнаем потомков нашей вершины и вызываем от них рекурсивно этот же метод
        self.__cursor.execute("SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a))
        m = []
        res = self.__cursor.fetchone()
        while res is not None:
            m.append(res[0])
            res = self.__cursor.fetchone()

        for i in m:
            self.deletion_with_subtree(i)

        #удаляем все ребра нашей вершины (удаляем нашу вершину)
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a) + " OR " + self.__descendant + " = " + str(a))

    # a - куда, b - вставляемая вершина
    def insert(self, a, b):
        #проверка на то, что вставляемой на данный момент вершины не существует
        self.__cursor.execute("SELECT COUNT(" + self.__descendant + ") FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(b))
        if self.__cursor.fetchone()[0] != 0:
            print("такая вершина уже существует!")
        else:
            self.__cursor.execute("INSERT INTO " + self.__tableName + " VALUES (" + str(a) + ", " + str(b) + ")")

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def transfering_with_subtree(self, a, b):
        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(a))
        Q = self.__cursor.fetchone()[0]
        self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__descendant + " = " + str(a) + ", " + self.__ancestor + " = " + str(b) + " WHERE " + self.__descendant + " = " + str(a) + " AND " + self.__ancestor + " = " + str(Q))

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def transfering_without_subtree(self, a, b):
        self.deletion_without_subtree(a)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES (" + str(b) + ", " + str(a) + ")")

    def random_tree(self, a):
        self.__cursor.execute("DELETE FROM " + self.__tableName)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES (1, 1)")
        for i in range(1, a):
            self.insert(random.randint(1, i), i+1)

    def getGraph(self, G):
        nodes = set()
        self.__cursor.execute("SELECT DISTINCT " + self.__ancestor + " FROM " + self.__tableName)
        res = self.__cursor.fetchone()
        while res is not None:
            nodes.add(res[0])
            res = self.__cursor.fetchone()
        self.__cursor.execute("SELECT DISTINCT " + self.__descendant + " FROM " + self.__tableName)
        res = self.__cursor.fetchone()
        while res is not None:
            nodes.add(res[0])
            res = self.__cursor.fetchone()
        # Выше происходит занесение в массив nodes всех различных вершин

        # Создание всех этих вершин в графе G
        for i in nodes:
            G.add_node(str(i))

        # Создание всех ребер вершин по записям таблицы (предок -> наследник)
        self.__cursor.execute("SELECT * FROM " + self.__tableName)
        res = self.__cursor.fetchone()
        while res is not None:
            G.add_edge(str(res[0]), str(res[1]))
            res = self.__cursor.fetchone()

        return G
"""
" + self.__tableName + "
" + self.__ancestor + "
" + self.__descendant + "
"""
