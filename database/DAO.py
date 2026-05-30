from database.DB_connect import DBConnect
from model.arco import Arco
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from categories"

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductByCategory(c):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from products p where p.category_id = %s"

        cursor.execute(query,(c.category_id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(c, d1, d2, idMapP):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.product_id as id1, t2.product_id as id2, t1.n as nt1, t2.n as nt2, t1.n+t2.n as peso
                    FROM (select p.product_id, count(*) as n
                    from orders o, order_items oi, products p
                    where o.order_id = oi.order_id 
                    and oi.product_id = p.product_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) t1,
                    (select p.product_id, count(*) as n
                    from orders o, order_items oi, products p
                    where o.order_id = oi.order_id 
                    and oi.product_id = p.product_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) t2
                    WHERE t1.product_id <>t2.product_id 
                    AND t1.n >= t2.n
                    ORDER BY peso DESC"""

        cursor.execute(query, (d1, d2, c.category_id, d1, d2, c.category_id))

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]], idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results