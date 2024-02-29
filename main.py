from distutils.log import debug 
from fileinput import filename 
from flask import *  

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="A;sldkfj14321",
  db = "wardrobe"
)



app = Flask(__name__)  

@app.route('/')   
def main():   
    return render_template("home_page.html")   
  
@app.route('/Add_Product')   
def addprod():   
    return render_template("add_cloth.html")   

  
@app.route('/Add_Product', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['user_image'] 
        f.save("./static/images/"+ f.filename)

        # getting input with name = fname in HTML form
        item_name = request.form.get("item_name")
        # getting input with name = lname in HTML form 
        color_name = request.form.get("color_name") 

        type_name = request.form.get("type")

        mycursor = mydb.cursor()

        sql = "INSERT INTO wardrobe (itemname, color, type, imagename) VALUES (%s, %s, %s, %s)"
        val = (item_name, color_name, type_name, f.filename)
        mycursor.execute(sql, val)

        mydb.commit()

        return redirect("/wardrobe")


@app.route('/wardrobe', methods = ['GET'])   
def wardrobe():

    mycursor = mydb.cursor()
    sql = "select * from wardrobe"
    mycursor.execute(sql)
    L = mycursor.fetchall()

    Data = []

    for i in L:
        Dict = {}
        Dict['name'] = i[1]
        Dict['color'] = i[2]
        Dict['type'] = i[3]
        Dict['image_link'] = i[4]

        Data.append(Dict)
    

    return render_template("wardrobe.html", length = len(L), data=Data)  
    
if __name__ == '__main__':   
    app.run(debug=True)
