from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
import os

app = Flask(__name__)

productobjects = []

class product:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.image = name+".jpg" 


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  database="products"
  
)

cursor = mydb.cursor()
cursor.execute("SELECT * FROM `product`")
records = cursor.fetchall()
for i in records:
    productobjects.append(product(i[0], i[1], i[2], i[3]))



@app.route("/")
def hello_world():

    return render_template('index.html')

@app.route("/cleardb")
def cleardb():
    cursor.execute("DELETE FROM `product`")
    mydb.commit()
    productobjects=[]
    return "Database cleared"

@app.route("/products")
def products():
    productobjects=[]
    cursor.execute("SELECT * FROM `product`")
    records = cursor.fetchall()
    for i in records:
        productobjects.append(product(i[0], i[1], i[2], i[3]))
    return render_template('products.html', prods=productobjects)

@app.route("/product/<id>")
def show_product(id):
    for i in productobjects:
        if i.name == str(id):
            return render_template('product.html', prod=i)
    return "Product not found"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    
    if request.method=="POST":
       
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
       
        if name=="" or price=="" or description=="":
            return "Please fill all the fields"
        cursor.execute(f"INSERT INTO `product` (`name`, `price`, `des`) VALUES ('{name}', '{price}', '{description}')")
        mydb.commit()
        if len(productobjects)==0:
            productobjects.append(product(1, name, price, description))
        else:
            productobjects.append(product(productobjects[-1].id+1, name, price, description))
        return "Produkt tilføjet til database. Tilføj et billede til produktet i mappen 'static' og navngiv det samme som produktet."
        
    return render_template('admin.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')