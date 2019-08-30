import mysql.connector
from config import password
mydb = mysql.connector.connect(host = "localhost", user = "root",passwd = password , database = "user_cripts")
mycursor = mydb.cursor()