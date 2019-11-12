import random

class Neighbors(Tree):
    def __init__(self, cursor, columns, tableName):
        self.__ancestor = columns[0]
        self.__descendant = columns[1]
        self.__tableName = tableName
        self.__cursor = cursor

    """
    def random_tree(self, a):
        self.__cursor.execute("DELETE FROM " + self.__tableName)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES (1, 1)")
        for i in range(1, a):
            self.insert(random.randint(1, i))
    """

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
        Q = self.__cursor.fetchone()

        # удаляем нашу вершину, а ребра от нее к своим потомкам перекидываем на ее предка (Q)
        for node in subtree:
            self.__cursor.execute("UPDATE " + self.__tableName + "SET(" + Q + ", " + node + ") WHERE " + self.__ancestor + " = " + a + " AND " + self.__descendant + " = " + node)
        self.__cursor.execute("DELETE FROM " + self.__tableName + "WHERE " + self.__descendant + " = " + a)
    
    def deletion_with_subtree(self, a):
        #узнаем потомков нашей вершины и вызываем от них рекурсивно этот же метод
        self.__cursor.execute("SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + a)
        res = self.__cursor.fetchone()
        while res is not None:
            deletion_with_subtree(res[0])
            res = self.__cursor.fetchone()

        #удаляем все ребра нашей вершины (удаляем нашу вершину)
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + a + " OR " + self.__descendant + " = " + a)

    # a - куда, b - вставляемая вершина
    def insert(self, a, b):
        #проверка на то, что вставляемой на данный момент вершины не существует
        self.__cursor.execute("SELECT COUNT(" + self.__descendant + ") FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + b)
        if self.__cursor.execute()[0] != 0:
            print("такая вершина уже существует!")
        else:
            self.__cursor.execute("INSERT INTO " + self.__tableName + " VALUES (" + a + ", " + b + ")")

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def transfering_with_sutree(self, a, b):
        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + a)
        Q = self.__cursor.fetchone()[0]
        self.__cursor.execute("UPDATE " + self.__tableName + " SET (" + a + ", " + b + ") WHERE " + self.__descendant + " = " + a + " AND " + self.__ancestor + " = " + Q)

    def trensfering_without_subtree(self, a, b):
        deletion_without_subtree(a)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES (" + b + ", " + a + ")")

    

"""
" + self.__tableName + "
" + self.__ancestor + "
" + self.__descendant + "
"""
