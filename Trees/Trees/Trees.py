from mysql.connector import MySQLConnection, Error
from NewFolder1.python_mysql_dbconfig import read_db_config

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

dbconfig = read_db_config()

def create(tableName):
    column_names = []
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = " + "'" + tableName + "'")
    column = cursor.fetchone()
    while column is not None:
        column_names.append(column[0])
        column = cursor.fetchone()
    if tableName == 'closures':
        from Classes.Closures import Closures
        return Closures(cursor, column_names, tableName)
    if tableName == 'neighbors':
        from Classes.Neighbors import Neighbors
        return Neighbors(cursor, column_names, tableName)
    if tableName == 'nested_sets':
        from Classes.Nested_sets import Nested_sets
        return Nested_sets(cursor, column_names, tableName)
    if tableName == 'paths':
        from Classes.Paths import Paths
        return Paths(cursor, column_names, tableName)
        

if __name__ == '__main__':
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        c = create('paths')
        conn.commit()
        G = c.getGraph(nx.DiGraph())
        plt.title('my_tree')
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.savefig('nx_test.png')
        plt.show()
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    