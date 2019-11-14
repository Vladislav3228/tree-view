import random
class Closures():
    def __init__(self, cursor, columns, tableName):
        self.__ancestor = columns[0]
        self.__descendant = columns[1]
        self.__tableName = tableName
        self.__cursor = cursor

    # " + self.__tableName + "
    # " + self.__ancestor + "
    # " + self.__descendant + "

    def random_tree(self, a):
        self.__cursor.execute("DELETE FROM " + self.__tableName)
        self.__cursor.execute("INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES (1, 1)")
        for i in range(1, a):
            self.insert(random.randint(1, i))
    def deletion_without_subtree(self, a):
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a) + " OR " + self.__descendant + " = " + str(a))

    def deletion_with_subtree(self, a):
        self.__cursor.execute("SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a))
        des = self.__cursor.fetchone()
        y = []
        while des is not None:
            y.append(des[0])
            des = self.__cursor.fetchone()
        i = len(y)
        for i in range(0, len(y)):
            self.deletion_without_subtree(y[i]) 

    def insert(self, a):
        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(a))
        anc = self.__cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self.__cursor.fetchone()
        self.__cursor.execute("SELECT MAX(" + self.__ancestor + ") FROM " + self.__tableName)
        new_number = self.__cursor.fetchone()[0] + 1
        x.append(new_number)
        i = 0
        insert_request = "INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES "
        while i < len(x):
            insert_request += "(" + str(x[i]) + ", " + str(new_number) + "),"
            i += 1
        self.__cursor.execute(insert_request[:-1])

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def transfering_without_subtree(self, a, b):
        self.__cursor.execute("DELETE FROM " + self.__tableName + " WHERE " + self.__ancestor + " != " + self.__descendant + " AND (" + self.__ancestor + " = " + str(a) + " OR " + self.__descendant + " = " + str(a) + ")")

        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(b))
        anc = self.__cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self.__cursor.fetchone()
        i = 0
        insert_request = "INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES "
        while i < len(x):
            insert_request += "(" + str(x[i]) + ", " + str(a) + "),"
            i += 1
        self.__cursor.execute(insert_request[:-1])

    #'a' - какую вершину берем для переноса, 'b' - под какую вершину переносим
    def transfering_with_subrtee(self, a, b):
        s1 = "DELETE FROM " + self.__tableName + " WHERE " + self.__ancestor + " IN (SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(a) +" AND " + self.__ancestor + " != " + str(a) + ") AND " + self.__descendant + " IN (SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a) + ")"
        self.__cursor.execute(s1)
        self.__cursor.execute("SELECT " + self.__ancestor + " FROM " + self.__tableName + " WHERE " + self.__descendant + " = " + str(b))
        anc = self.__cursor.fetchone()
        x = []
        while anc is not None:
            x.append(anc[0])
            anc = self.__cursor.fetchone()
        self.__cursor.execute("SELECT " + self.__descendant + " FROM " + self.__tableName + " WHERE " + self.__ancestor + " = " + str(a))
        des = self.__cursor.fetchone()
        y = []
        while des is not None:
            y.append(des[0])
            des = self.__cursor.fetchone()
        i = 0
        j = 0
        insert_request = "INSERT INTO " + self.__tableName + " (" + self.__ancestor + ", " + self.__descendant + ") VALUES "
        for i in range(len(y)):
            for j in range(len(x)):
                insert_request += "(" + str(x[j]) + ", " + str(y[i]) + "),"           
        self.__cursor.execute(insert_request[:-1])

    

    def getGraph(self, G):
        anc = []
        self.__cursor.execute("SELECT DISTINCT " + self.__ancestor + " FROM " + self.__tableName)
        row = self.__cursor.fetchone()
        while row is not None:
            anc.append(row[0])
            G.add_node(str(row[0]))
            row = self.__cursor.fetchone()
        data = []
        self.__cursor.execute("SELECT * FROM " + self.__tableName)
        row = self.__cursor.fetchone()
        while row is not None:
            data.append(row)
            row = self.__cursor.fetchone()
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
