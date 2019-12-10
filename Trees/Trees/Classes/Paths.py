import random

"""
" + self.__node + "
" + self.__path + "
" + self.__tableName + "
"""

class Paths():
    def __init__(self, cursor, columns, tableName):
        self.__node = columns[0]
        self.__path = columns[1]
        self.__tableName = tableName
        self.__cursor = cursor

    def insert(self, to, node):
        self.__cursor.execute("SELECT " + self.__path + " FROM " + self.__tableName + " WHERE " + self.__node + " = '" + to + "'")
        path = self.__cursor.fetchone()[0] + "/" + node
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__node + ", " + self.__path + ") VALUES ('" + node + "', '" + path + "')")

    def del_node(self, node):
        self.__cursor.execute("SELECT " + self.__path + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + node)
        check = self.__cursor.fetchone()[0]
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__node + " = " + node)
        if check == node:
            self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__path + " = REPLACE(" + self.__path + ", '" + node + "/', '') WHERE " + self.__path + " REGEXP '" + node + "/'")
        else:
            self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__path + " = REPLACE(" + self.__path + ", '" + node + "/', '') WHERE " + self.__path + " REGEXP '/" + node + "/'")

    def del_sbtr(self, node):
        self.__cursor.execute("SELECT " + self.__path + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + node)
        check = self.__cursor.fetchone()[0]
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__node + " = " + node)
        if check == node:
            self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__node + " REGEXP '" + node + "/'")
        else:
            self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__node + " REGEXP '/" + node + "/'")
           
    def move_node(self, node, to):
        self.del_node(node)
        self.insert(to, node)

    def move_sbtr(self, node, to):
        self.__cursor.execute("SELECT " + self.__path + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + node)
        n = self.__cursor.fetchone()[0]
        self.__cursor.execute("SELECT " + self.__path + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + to)
        m = self.__cursor.fetchone()[0]
        self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__path + " = '" + m + "/" + node + "' WHERE " + self.__node + " = " + node)
        self.__cursor.execute("UPDATE " + self.__tableName + " SET " + self.__path + " = REPLACE(" + self.__path + ", '" + n + "', '" + m + "/" + node + "') WHERE " + self.__path + " REGEXP '" + n + "'")

    def random_tree(self, count):
        self._cursor.execute("DELETE FROM " + self._tableName)
        self._cursor.execute("INSERT INTO " + self._tableName + " (" + self.__node + ", " + self.__path + ") VALUES (1, 1)")
        for i in range(1, count):
            self.insert(random.randint(1, i))


    """
    def getEdges(self, G, i):
        self.__cursor.execute("SELECT " + self.__node + " FROM " + self.__tableName + " WHERE " + self.__path + " REGEXP '" + i + "/.$'")
        mn = set()
        res = self.__cursor.fetchone()
        while res is not None:
            mn.add(res[0])
            res = self.__cursor.fetchone()
        for elem in mn:
            G.add_edge(i, elem)
            self.getEdges(G, elem)

    def getGraph(self, G):
        self.__cursor.execute("SELECT " + self.__node + ", " + self.__path+ " FROM " + self.__tableName)
        res = self.__cursor.fetchone()
        while res is not None:
            G.add_node(res[0])
            res = self.__cursor.fetchone()
        self.__cursor.execute("SELECT " + self.__node + " FROM " + self.__tableName + " WHERE " + self.__node + " = " + self.__path)
        root = self.__cursor.fetchone()
        while root is not None:
            self.getEdges(G, root[0])
            root = self.__cursor.fetchone()
        return G
    """
    def getEdges(self, G, root, data):
        for str in data:
            print(data[str])
            u = data[str].split('/')
            if len(u) != 1:
                if u[len(u)-2] == root:
                    print(u)
                
                    G.add_edge(root, u[len(u)-1])
                    self.getEdges(G, u[len(u)-1], data)
        print('-----------------------------------------')
   
    def getGraph(self, G):
        data = {}
        self.__cursor.execute("SELECT " + self.__node + ", " + self.__path + " FROM " + self.__tableName)
        res = self.__cursor.fetchone()
        while res is not None:
            G.add_node(res[0])
            q = {res[0]: res[1]}
            data.update(q)
            res = self.__cursor.fetchone()
        print(data)
        for key in data:
            if key == data[key]:
                self.getEdges(G, key, data)
        return G

