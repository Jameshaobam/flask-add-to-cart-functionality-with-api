"""
This project was created by Haobam Jameskumar singh

email- haobamjamess8@gmail.com

"""



from flask import Flask, jsonify, request,render_template,redirect
from mysql_control import MysqlConnect
app = Flask(__name__,template_folder='template')



@app.route("/products",methods=['GET'])
def products():

    return render_template('index.html')

@app.route("/",methods=['GET'])
def home():
    return redirect('products')

@app.route("/carts",methods=['GET'])
def carts():

    return render_template('carts.html')

@app.route("/checkout",methods=['GET'])
def checkout_page():
    if 'addrs' in request.args:
        print(request.args['addrs'])
        addrs = request.args['addrs']
    if 'totalprice' in request.args:
        
        totalprice = request.args['totalprice']
        print(totalprice)
        data={
            'addrs':addrs,
            'totalprice':totalprice
        }
    else:
        data={
            'status':"Address not provided",
            'totalprice':totalprice
        }
   
    return render_template('checkout.html',data=data)


@app.route("/v1/product/all",methods=['GET'])
def get_all_prd_url():
    mysql_connect = MysqlConnect()
    output = mysql_connect.get_all_products()
    datas=[]
    for item in output:
        datas.append({'prd_id': item[0], 'prd_title': item[1],'prd_price':item[2]})
    return jsonify({'datas':datas})

@app.route("/v1/cart/all", methods=['GET'])
def get_all_cart_url():
    mysql_connect = MysqlConnect()
    output,totalprice= mysql_connect.get_all_cart()

    datas=[]

    for item in output:
        datas.append({'cart_id': item[0],'cart_title':item[1],'cart_price':item[2]})

    return jsonify({'datas':datas,'total':len(datas),'totalprice':totalprice})

@app.route('/v1/cart/add',methods=['GET'])
def add_to_cart():
    if 'id' in request.args:
        print(request.args['id'])
        id = int(request.args['id'])
    else:
        data={
            'status':"No such data"
        }
        return jsonify(data)
    
    mysql =   MysqlConnect()
    msg,totalprice = mysql.addto_cart(id=id)

    data={
        'status':msg,
        'total_price':totalprice
    }

    return jsonify(data)
@app.route('/v1/cart/delete',methods=['GET'])
def delete_cart():
    if 'id' in request.args:
        print(request.args['id'])
        id = int(request.args['id'])
    else:
        data={
            'status':"No such data"
        }
        return jsonify(data)
    mysql =   MysqlConnect()
    msg = mysql.delete_from_cart(id=id)

    data={
        'status':msg,
    }

    return jsonify(data)


@app.route('/v1/checkout',methods=['GET']) #url/v1/checkout?addrs=someaddress&totalprice=499.0
def checkout():
    if 'addrs' in request.args:
        print(request.args['addrs'])
        addrs = request.args['addrs']
    if 'totalprice' in request.args:
        
        totalprice = request.args['totalprice']
        print(totalprice)
        data={
            'addrs':addrs,
            'totalprice':totalprice
        }
    else:
        data={
            'status':"Address not provided"
        }
    return jsonify(data)
    

        
    

if __name__ == '__main__':
    app.run(debug=True)