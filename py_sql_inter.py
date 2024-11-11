import cx_Oracle
from tabulate import tabulate
class DatabaseAccess:
    def init(self, username, password):
        self.username = username
        self.password = password
        self.connected = False
        self.con = None
    def connect(self):
        try:
            self.con = cx_Oracle.connect(self.username, self.password, "localhost:1521/xe")
            self.connected = True
            print("The database is connected to python succesfully.")
        except cx_Oracle.DatabaseError as e:
            print("Please check your login credentials once again, they aren't correct.")
    def execute_sql(self, sql):
        if not self.connected:
            print("The database is not connected.")
            return
        try:
            cur = self.con.cursor()
            cur.execute(sql)
            if sql.strip().lower().startswith('select'):
                rows = cur.fetchall()
                headers = [col[0] for col in cur.description]
                print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
            else:
                print("The query executed succesfully and operation done.")
                self.con.commit()
            cur.close()
        except cx_Oracle.DatabaseError as e:
            print("Error in executing the sql query.", e)
    def close_connection(self):
        if self.connected:
            try:
                self.con.close()
                print("The connection between python and sql closed succesfully.")
            except cx_Oracle.DatabaseError as e:
                print("The connection is not closed.")
def main():
    username = input("Username: ")
    password = input("Password: ")
    dba = DatabaseAccess(username, password)
    dba.connect()
    while dba.connected:
        print("\nEnter your choice")
        print("1. Enter SQL query.")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '2':
            dba.close_connection()
            break
        if choice == '1':
            sql_statement = input("Enter SQL statement: ")
            sql_statement = sql_statement.rstrip(';')
            dba.execute_sql(sql_statement)
if name == "main":
    main()