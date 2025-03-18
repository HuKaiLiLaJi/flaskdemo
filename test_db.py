import MySQLdb



DB_HOST = "database-onboarding.cr08a2i6ah44.ap-southeast-2.rds.amazonaws.com"

DB_USER = "admin"
DB_PASS = "TA03Onboarding"
DB_NAME = "database-onboarding"
DB_PORT = 1433


try:
    conn = MySQLdb.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME
    )
    print("Connection successful")
except MySQLdb.OperationalError as e:
    print(f"Error: {e.args}")  
    print(f"Error Code: {e.args[0]}")
    print(f"Error Message: {e.args[1]}")
