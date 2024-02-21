from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/products", methods = ['GET'])
def getProducts():
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM Product")

        rows = cur.fetchall()
        con.close()
        products = []
        for row in rows:
            product = {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": row[3],
                "image_url": row[4]
            }
            products.append(product)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify(products)

@app.route("/products/<id>", methods = ['GET'])
def getProduct(id):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM Product WHERE id="+id)

        row = cur.fetchall()
        con.close()
        # product = {
        #     "id": row[0],
        #     "name": row[1],
        #     "description": row[2],
        #     "price": row[3],
        #     "image_url": row[4]
        # }
        
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    return jsonify(row)

@app.route("/cart", methods = ['POST','GET'])
def cart():
    if request.method=='POST':
        #Adds a product to the cart
        content = request.get_json(silent=False)
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            product_id = content['product_id']
            quantity = content['quantity']

            cur.execute("INSERT INTO CartItem (product_id, quantity) VALUES (?, ?)",
                        (product_id,quantity))
            
            con.commit()
            con.close()

            return jsonify({"message": "Product added to Cart successfully"}), 201
        
        except KeyError:
            return jsonify({"error": "Invalid JSON data"}), 400
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        
    try:
        #Retrieves the cart items.
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM CartItem")

        rows = cur.fetchall()
        con.close()
        CartItems = []
        for row in rows:
            cart = {
                "id": row[0],
                "product_id": row[1],
                "quantity": row[2],
            }
            CartItems.append(cart)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify(CartItems)

@app.route("/cart/<id>", methods = ['POST'])
def removeItem(id):
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM CartItem where id="+id)
        con.commit()
        msg = f'CartItem of id {id} deleted successfully'
        return jsonify({"message": msg}), 201
    
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except:
        con.rollback()
        return jsonify({"message": "Error in delete"})
    finally:
        con.close()
    
    


@app.route("/add-product", methods = ['POST'])
def addProduct():
    content = request.get_json(silent=False)
    try:
        name = content['name']
        description = content['description']
        price = content['price']
        image_url = content['image_url']

        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO Product (name, description, price, image_url) VALUES (?, ?, ?, ?)",
                    (name, description, price, image_url))
        
        con.commit()
        con.close()

        return jsonify({"message": "Product added successfully"}), 201
    
    except KeyError:
        return jsonify({"error": "Invalid JSON data"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
