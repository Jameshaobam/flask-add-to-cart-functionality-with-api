import pymysql

class MysqlConnect:

    def __init__(self):
        # To connect MySQL database
        self.conn = pymysql.connect(
            host='localhost',
            user='root', 
            password = "1234",
            db='ecom',
            )
        
        self.cur = self.conn.cursor()
        
    def get_all_cart(self):
        query="Select * from cart;"
      
        self.cur.execute(query)
        output = self.cur.fetchall()
        total_price = self.get_total_price()
        print(total_price)
        print(output)
        return output,total_price

    def get_total_price(self):

        query="""select count(*) from cart """
        self.cur.execute(query)
        count = self.cur.fetchone()
        print(count)
        for i in count:
            print(i)
        if count[0] >= 1:
            query_total_price = """Select SUM(price) from cart;"""
            self.cur.execute(query_total_price)
            total_price = self.cur.fetchone()
            return round(total_price[0],2)
        else:
            return 0



    def addto_cart(self,id=None):
        query = """create table if not exists cart(cart_id int primary key,
        title varchar(255),price float);
        """
        self.cur.execute(query)
        print(type(id))
        query="""select count(*) from cart where cart_id ={}""".format(id)
        self.cur.execute(query)
        count = self.cur.fetchone()
        print(count)
        for i in count:
            print(i)
        if count[0] >= 1:
            print("Item already in the cart")
            return "Item already in the cart",self.get_total_price()
        else:
            query="""select * from products where prd_id={}""".format(id)
            self.cur.execute(query)
            record =  self.cur.fetchone()
            if record == None:
                print("Product does not exists")
                return "Product does not exists",self.get_total_price()

            else:
                query="""INSERT INTO cart VALUES({},{},{})""".format(repr(record[0]),repr(record[1]),repr(record[2]))
                self.cur.execute(query)
                self.conn.commit()
                print("Item has been added to cart")
                total_price = self.get_total_price()
                return "Item has been added to cart",total_price

    def delete_from_cart(self,id):
        query="Delete from cart where cart_id={};".format(id)
      
        self.cur.execute(query)
        self.conn.commit()
        print(f"Item {id} has been deleted from cart")
        return f"Item {id} will been delete from cart"
    
    def get_all_products(self):
        query="Select * from products;"
      
        self.cur.execute(query)
        output = self.cur.fetchall() 
        print(output)
        return output
            
         

    
  
# Driver Code
if __name__ == "__main__" :
    mysql_connect = MysqlConnect()
    mysql_connect.addto_cart(id=1)
    mysql_connect.get_all_cart()