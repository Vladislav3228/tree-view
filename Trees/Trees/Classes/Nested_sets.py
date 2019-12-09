import random

ex_nodes = set()

class Nested_sets():
    def __init__(self, cursor, columns, tableName):
        self.__node = columns[0]
        self.__leftSide = columns[1]
        self.__rightSide = columns[2]
        self.__tableName = tableName
        self.__cursor = cursor

    def del_sbtr(self, a):
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__node + " = " + str(a))

    def del_node(self, a):
        self.__cursor.execute("SELECT left, right FROM " + self.__tableName + " WHERE " + self.__node + " = " + str(a))
        lr = self.__cursor.fetchone()
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__leftSide + " >= " + str(lr[0]) + " AND " + self.__rightSide + " <= " + str(lr[1]))

    def insert(self, a, b):
        self.__cursor.execute("SELECT " + self.__leftSide + ", " + self.__rightSide + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + str(a))
        n = self.__cursor.fetchone()
        self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__leftSide + " = " + self.__leftSide + " + 2 WHERE " + self.__leftSide + " > " + str(n[0]))
        self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__rightSide + " = " + self.__rightSide + " + 2 WHERE " + self.__rightSide + " > " + str(n[0]))
        self.__cursor.execute("INSERT INTO " + self.__tableName + " VALUES (" + str(b) + ", " + str(n[0]+1) + ", " + str(n[0]+2) + ")")

    def getGraph(self, G):
        
        lists = []
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + self.__rightSide + " = " + self.__leftSide + " + 1")
        row = self.__cursor.fetchone()
        while row is not None:
            lists.append(row)
            row = self.__cursor.fetchone()
        for i in lists:
            G.add_node(i[0])
            self.__graphFunc(G, i)
        return G

    def __graphFunc(self, G, i):
        self.__cursor.execute("SELECT * FROM " + self.__tableName + " WHERE " + self.__leftSide + " = ( SELECT MAX(" + self.__leftSide + ") FROM " + self.__tableName + " WHERE " + self.__leftSide + " < " + str(i[1]) + " AND " + self.__rightSide + " > " + str(i[2]) + ")")
        u = self.__cursor.fetchone()
        if u not in ex_nodes:
            ex_nodes.add(u)
            G.add_node(u[0])
            if u[1] != 1:
                self.__graphFunc(G, u)
        G.add_edge(u[0], i[0])

"""
" + self.__node + "
" + self.__leftSide + "
" + self.__rightSide + "
" + self.__tableName + "
"""