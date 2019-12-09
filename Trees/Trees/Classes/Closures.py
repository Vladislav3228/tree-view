import random

class Closures():

    def __init__(self, cursor, columns, tableName):
        self._ancestor = columns[0]
        self._descendant = columns[1]
        self._tableName = tableName
        self._cursor = cursor

    def random_tree(self, a):
        self._cursor.execute("DELETE FROM " + self._tableName)
        self._cursor.execute("INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES (1, 1)")
        for i in range(1, a):
            self.insert(random.randint(1, i))

    def del_node(self, a):
        self._cursor.execute("DELETE FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a) + " OR " + self._descendant + " = " + str(a))

    def del_sbtr(self, a):
        self._cursor.execute("SELECT " + self._descendant + " FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a))
        des = self._cursor.fetchone()
        y = []
        while des is not None:
            y.append(des[0])
            des = self._cursor.fetchone()
        i = len(y)
        for i in range(0, len(y)):
            self.del_node(y[i]) 

    def insert(self, a):
        self._cursor.execute("SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(a))
        anc = self._cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self._cursor.fetchone()
        self._cursor.execute("SELECT MAX(" + self._ancestor + ") FROM " + self._tableName)
        new_number = self._cursor.fetchone()[0] + 1
        x.append(new_number)
        i = 0
        insert_request = "INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES "
        while i < len(x):
            insert_request += "(" + str(x[i]) + ", " + str(new_number) + "),"
            i += 1
        self._cursor.execute(insert_request[:-1])

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def move_node(self, a, b):
        self._cursor.execute("DELETE FROM " + self._tableName + " WHERE " + self._ancestor + " != " + self._descendant + " AND (" + self._ancestor + " = " + str(a) + " OR " + self._descendant + " = " + str(a) + ")")

        self._cursor.execute("SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(b))
        anc = self._cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self._cursor.fetchone()
        i = 0
        insert_request = "INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES "
        while i < len(x):
            insert_request += "(" + str(x[i]) + ", " + str(a) + "),"
            i += 1
        self._cursor.execute(insert_request[:-1])

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def move_sbtr(self, a, b):
        s1 = "DELETE FROM " + self._tableName + " WHERE " + self._ancestor + " IN (SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(a) +" AND " + self._ancestor + " != " + str(a) + ") AND " + self._descendant + " IN (SELECT " + self._descendant + " FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a) + ")"
        self._cursor.execute(s1)
        self._cursor.execute("SELECT " + self._ancestor + " FROM " + self._tableName + " WHERE " + self._descendant + " = " + str(b))
        anc = self._cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self._cursor.fetchone()
        self._cursor.execute("SELECT " + self._descendant + " FROM " + self._tableName + " WHERE " + self._ancestor + " = " + str(a))
        des = self._cursor.fetchone()
        y = []
        while des is not None:
            y.append(des[0])
            des = self._cursor.fetchone()
        i = 0
        j = 0
        insert_request = "INSERT INTO " + self._tableName + " (" + self._ancestor + ", " + self._descendant + ") VALUES "
        for i in range(len(y)):
            for j in range(len(x)):
                insert_request += "(" + str(x[j]) + ", " + str(y[i]) + "),"           
        self._cursor.execute(insert_request[:-1])

    

    def getGraph(self, G):
        anc = []
        self._cursor.execute("SELECT DISTINCT " + self._ancestor + " FROM " + self._tableName)
        row = self._cursor.fetchone()
        while row is not None:
            anc.append(row[0])
            G.add_node(str(row[0]))
            row = self._cursor.fetchone()
        data = []
        self._cursor.execute("SELECT * FROM " + self._tableName)
        row = self._cursor.fetchone()
        while row is not None:
            data.append(row)
            row = self._cursor.fetchone()
        INF = -10000
        mtrx = {}
        for i in anc:
            for j in anc:
                if i in mtrx:
                    mtrx[i][j] = INF
                else:
                    q = {i: {j: INF}}
                    mtrx.update(q)
        for elem in data:
            if(elem[0] == elem[1]):
                if(elem[0] != anc[0]):
                    mtrx[elem[0]][elem[1]] = INF
                else:
                    mtrx[elem[0]][elem[1]] = 0
            else:
                mtrx[elem[0]][elem[1]] = 1
        for k in range(1, len(anc)):
            for i in anc:
                for j in anc:
                    if(mtrx[i][j] < (mtrx[i][anc[k]] + mtrx[anc[k]][j])):
                        mtrx[i][j] = mtrx[i][anc[k]] + mtrx[anc[k]][j]
        #дабы не проходиться по всей матрице, прохожусь по date, где записаны все пары вершин нашей базы, чтобы найти те пары, вес между которыми в матрице mtrx равен единице, после чего добавляю соответсвующее ребро в наш граф G
        for elem in data:
            if(mtrx[elem[0]][elem[1]] == 1):
                G.add_edge(str(elem[0]), str(elem[1]))
        return G