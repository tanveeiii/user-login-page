from flask import Flask, session
from flask_mysqldb import MySQL
from flask import render_template, request, redirect 
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('HOST')
app.config['MYSQL_USER'] = os.getenv("USER")
app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def login():
   if(request.method=="GET"):
      return render_template("login.html")
   elif(request.method=="POST"):
      userid = request.form["userid"]
      password = request.form["password"]
      cursor = mysql.connection.cursor()
      query = f"SELECT * FROM userDetails WHERE userid = '{userid}' AND password = '{password}'"
      cursor.execute(query)
      account = cursor.fetchone()
      if account:
         session["name"] = userid
         return render_template("welcome.html", userid=userid)
      else:
         error="The username or password is incorrect!!"
         return render_template("login.html", error=error)
      

@app.route("/signup", methods=['GET', 'POST'])
def signup():
   if(request.method=='GET'):
      return render_template("signup.html")
   elif(request.method=='POST'):
      userid = request.form['userid']
      phone = request.form["phone"]
      password = request.form['password']
      confirm = request.form['confirm']
      if(password==confirm):
         cursor = mysql.connection.cursor()
         query = f"INSERT INTO userDetails VALUES('{userid}',{phone},'{password}')"
         cursor.execute(query)
         mysql.connection.commit()
         return render_template("welcome.html", userid=userid)
      else:
         error="Password and confirm password doesn't match!!"
         return render_template("signup.html", error=error)
      

@app.route("/welcome")
def welcome():
   return render_template("welcome.html")

@app.route("/logout")
def logout():
   session["name"] = None
   return redirect("/")


if __name__ == '__main__':
  app.run(debug=True)