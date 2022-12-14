"""Code for a flask API to Create, Read, Update, Delete users"""
import os
import io
import boto3
import json
from flask import jsonify, request, Flask, render_template, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = os.getenv("db_username")
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password") 
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name") 
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST") 
app.config["MYSQL_DATABASE_PORT"] = int('3306')
mysql.init_app(app)

# BackGround_Image = os.getenv("BG_IMG") 
Header = os.getenv("HEADER")

with open("/clo835/config/image_url") as f:
   text = f.read().replace("\n","")

BackGround_Image = text

AWS_REGION = "us-east-1"
S3_BUCKET_NAME = "k8s-sohel-images"
s3_resource = boto3.resource("s3", region_name=AWS_REGION)

s3_object = s3_resource.Object(S3_BUCKET_NAME, BackGround_Image)

s3_object.download_file('static/image.jpg')

object_url = "https://"+S3_BUCKET_NAME+".s3.amazonaws.com/"+BackGround_Image
print("Object URL : " + object_url)


@app.route("/")
def test():
    return render_template('unittesting.html')

@app.route("/home")
def index():
    """Function to test the functionality of the API"""
    return render_template('welcome.html', header=Header)


@app.route("/users", methods=["GET"])
def users():
    """Function to retrieve all users from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('showuser.html',content=rows, header=Header)
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/create", methods=["POST"])
def add_user():
    """Function to create a user to the MySQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    if name and email and pwd and request.method == "POST":
        sql = "INSERT INTO users(user_name, user_email, user_password) " \
              "VALUES(%s, %s, %s)"
        data = (name, email, pwd)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email and pwd")



@app.route("/user/<int:user_id>", methods=["GET"])
def user(user_id):
    """Function to get information of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_user():
    """Function to update a user in the MYSQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    user_id = json["user_id"]
    if name and email and pwd and user_id and request.method == "POST":
        # save edits
        sql = "UPDATE users SET user_name=%s, user_email=%s, " \
              "user_password=%s WHERE user_id=%s"
        data = (name, email, pwd, user_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("User updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, email and pwd")


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", user_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
